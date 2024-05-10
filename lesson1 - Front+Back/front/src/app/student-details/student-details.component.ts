import {Component, OnInit} from '@angular/core';
import {Student} from "../student";
import {ActivatedRoute} from "@angular/router";
import {ApiService} from "../api.service";

@Component({
  selector: 'app-student-details',
  templateUrl: './student-details.component.html',
  styleUrls: ['./student-details.component.css']
})
export class StudentDetailsComponent implements OnInit{
  student : Student
  updatedStudent : Student
  sexes = ["Male", "Female"]

  constructor(private route: ActivatedRoute, private service: ApiService) {
    this.student = {} as Student
    this.updatedStudent = {} as Student
  }

  ngOnInit():void{
    this.getStudent()
  }

  getStudent(){
    this.route.paramMap.subscribe(params => {
      const id = Number(params.get("id"))
      console.log(id);
      this.service.getStudentDetails(id).subscribe(data => {
        console.log(data);

        this.student.id = data.id
        this.student.name = data.name
        this.student.age = data.age
        this.student.sex = data.sex
      })
    })
  }

  updateStudent(){
    this.route.paramMap.subscribe(params => {
      const id = Number(params.get("id"))
      console.log(id);
      this.service.updateStudentDetails(id, this.updatedStudent).subscribe(data => {})
    })
  }

  deleteStudent(){
    this.route.paramMap.subscribe(params => {
      const id = Number(params.get("id"))
      console.log(id);
      this.service.deleteStudent(id).subscribe(data => {})
    })
  }


  onDelete(){
    this.deleteStudent()
  }
  onSubmit(){
    this.updateStudent()
    window.location.reload()
  }

}
