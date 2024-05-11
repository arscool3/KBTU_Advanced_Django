
from aiogram import Bot
import asyncio
import os
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from database.db import engine
from models import Order, UserChatID
from celery_conf import celery_app
import dramatiq
from dramatiq.brokers.redis import RedisBroker

SessionLocal = sessionmaker(bind=engine)

broker = RedisBroker(url="redis://localhost:6379")
dramatiq.set_broker(broker)


@dramatiq.actor()
def generate_and_send_report():
    asyncio.run(send_report())


async def send_report():
    db = SessionLocal()
    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    chat_id = 1782914764
    try:
        user = db.execute(select(UserChatID).where(UserChatID.chat_id == chat_id)).scalar_one()
        orders = db.execute(select(Order).where(Order.user_id == user.user_id)).scalars().all()

        report_text = "Your Orders Report:\n\n"
        for order in orders:
            report_text += f"Order ID: {order.id}, Total: {order.total_price}, Date: {order.order_date}\n"

        await bot.send_message(chat_id, report_text)

    except Exception as e:
        print(f"Failed to generate report: {str(e)}")
    finally:
        db.close()
        await bot.close()
#
# @dramatiq.actor()
# def generate_and_send_report():
#     db = SessionLocal()
#     print("22222")
#     bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
#     print("111111")
#     chat_id = 1782914764
#     try:
#         user = db.execute(select(UserChatID).where(UserChatID.chat_id == chat_id)).scalar_one()
#         orders = db.execute(select(Order).where(Order.user_id == user.user_id)).scalars().all()
#
#         report_text = "Your Orders Report:\n\n"
#         for order in orders:
#             report_text += f"Order ID: {order.id}, Total: {order.total_price}, Date: {order.order_date}\n"
#
#             bot.send_message(chat_id, report_text)
#
#     except Exception as e:
#         print(f"Failed to generate report: {str(e)}")
#     finally:
#         db.close()
#         bot.close()