import {Component, NgModule, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {ApiService} from "../api.service";
import {Student} from "../student";

@Component({
  selector: 'app-student-list',
  templateUrl: './student-list.component.html',
  styleUrls: ['./student-list.component.css'],
})

export class StudentListComponent implements OnInit{
  students : Student[]
  sexes = ["Male", "Female"]
  newStudent = {} as Student

  constructor(private route: ActivatedRoute, private service: ApiService) {
    this.students = [] as Student[]
  }

  ngOnInit():void{
    this.getStudents()
  }

  getStudents(){
    this.service.getStudents().subscribe((data) => {
      this.students = data
    })
  }

  onSubmit(){
    this.addStudent()
    window.location.reload()
  }

  addStudent(){
    this.service.addStudent(this.newStudent).subscribe((data) => {
      this.newStudent = data
    })
  }
}
