from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from database.db import Base, engine
from models.userModel import UserChatID, User, Product
from kafka.producer import send_to_kafka

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

SessionLocal = sessionmaker(bind=engine)


class Form(StatesGroup):
    name = State()
    email = State()
    phone_number = State()
    address = State()


class Form(StatesGroup):
    name = State()
    email = State()
    phone_number = State()
    address = State()
    ordering = State()


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await Form.name.set()
    await message.answer("Welcome to our registration bot!\nPlease enter your name:")


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.text
    await save_chat_id(username, user_id)
    async with state.proxy() as data:
        data['name'] = username
    await Form.next()
    await message.answer("What is your email?")


@dp.message_handler(state=Form.email)
async def process_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
    await Form.next()
    await message.answer("What is your phone number?")


@dp.message_handler(state=Form.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await Form.next()
    await message.answer("What is your address?")


@dp.message_handler(state=Form.address)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    await state.finish()
    await save_user(data)
    await message.answer("Thank you for registering!")


async def save_user(data):
    db = SessionLocal()
    try:
        new_user = User(name=data['name'], email=data['email'], phone_number=data['phone_number'], address=data['address'])
        db.add(new_user)
        db.commit()
        print("User saved successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()


async def save_chat_id(username: str, user_id: int):
    db = SessionLocal()
    try:
        existing_user = db.query(UserChatID).filter(UserChatID.username == username).first()
        if existing_user:
            return False
        new_user = UserChatID(username=username, chat_id=user_id)
        db.add(new_user)
        db.commit()
        return True
    finally:
        db.close()


@dp.message_handler(commands=['products'])
async def list_products(message: types.Message):
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        products_message = "\n".join(
            f"ID: {product.id} - {product.name} (${product.price})" for product in products
        )
        await message.answer("Here are our products:\n" + products_message)
    finally:
        db.close()


class Form(StatesGroup):
    name = State()
    email = State()
    phone_number = State()
    address = State()
    ordering = State()
    confirm_order = State()


@dp.message_handler(commands=['order'])
async def order_start(message: types.Message):
    await Form.ordering.set()
    await message.answer("Please enter the IDs of the products you wish to order, separated by commas:")


@dp.message_handler(state=Form.ordering)
async def process_order(message: types.Message, state: FSMContext):
    product_ids = message.text.split(',')
    db = SessionLocal()
    try:
        products = db.query(Product).filter(Product.id.in_([int(pid.strip()) for pid in product_ids if pid.strip().isdigit()])).all()
        if not products:
            await message.answer("No valid products found with the provided IDs.")
            await state.finish()
        else:
            order_details = "\n".join(f"{product.name}: ${product.price}" for product in products)
            async with state.proxy() as data:
                data['products'] = products
            await Form.confirm_order.set()
            await message.answer(f"You have selected the following products:\n{order_details}\nType 'confirm' to place your order or 'cancel' to abort.")
    except Exception as e:
        await message.answer("An error occurred while processing your order.")
        print(f"Error: {e}")
    finally:
        db.close()


@dp.message_handler(state=Form.confirm_order)
async def confirm_order(message: types.Message, state: FSMContext):
    if message.text.lower() == 'confirm':
        async with state.proxy() as data:
            await send_to_kafka(data['products'])
        await message.answer("Your order has been placed and sent for processing.")
        await state.finish()
    else:
        await message.answer("Order cancelled.")
        await state.finish()


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
