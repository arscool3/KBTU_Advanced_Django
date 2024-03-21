from fastapi import FastAPI, APIRouter
from app.container import get_container
from app.repository import DepartmentRepository, \
    EmployeeRepository, TaskRepository, ScheduleRepository
from app.dependencies import GetListDependency, DepartmentCreateDependency, \
    EmployeeCreateDependency, TaskCreateDependency, ScheduleCreateDependency

# App
app = FastAPI()

# Department
router_department = APIRouter(prefix="/department", tags=["Departments"])

router_department.add_api_route("/get_departments", get_container(DepartmentRepository).resolve(GetListDependency),
                                methods=["GET"])
router_department.add_api_route("/add_department",
                                get_container(DepartmentRepository).resolve(DepartmentCreateDependency),
                                methods=["POST"])
app.include_router(router_department)

# Employee
router_employee = APIRouter(prefix="/employee", tags=["Employees"])

router_employee.add_api_route("/get_employees", get_container(EmployeeRepository).resolve(GetListDependency),
                              methods=["GET"])
router_employee.add_api_route("/add_employee",
                              get_container(EmployeeRepository).resolve(EmployeeCreateDependency),
                              methods=["POST"])
app.include_router(router_employee)

# Task
router_task = APIRouter(prefix="/task", tags=["Tasks"])

router_task.add_api_route("/get_tasks", get_container(TaskRepository).resolve(GetListDependency),
                          methods=["GET"])
router_task.add_api_route("/add_task",
                          get_container(TaskRepository).resolve(TaskCreateDependency),
                          methods=["POST"])
app.include_router(router_task)

# Schedule
router_schedule = APIRouter(prefix="/schedule", tags=["Schedules"])

router_schedule.add_api_route("/get_schedules", get_container(ScheduleRepository).resolve(GetListDependency),
                              methods=["GET"])
router_schedule.add_api_route("/add_schedule",
                              get_container(ScheduleRepository).resolve(ScheduleCreateDependency),
                              methods=["POST"])
app.include_router(router_schedule)
