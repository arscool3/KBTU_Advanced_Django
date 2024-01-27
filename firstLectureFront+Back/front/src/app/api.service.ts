import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {Student} from "./student";

@Injectable({
  providedIn: 'root'
})

export class ApiService {
  BASE_URL = "http://127.0.0.1:8000/app/"
  constructor(private http: HttpClient) { }
  public getStudents() : Observable<Student[]>{
    return this.http.get<Student[]>(`${(this.BASE_URL)}`)
  }

  public addStudent(student: Student) : Observable<Student>{
    return this.http.post<Student>(`${(this.BASE_URL)}`, student)
  }

  public getStudentDetails(id: number) : Observable<Student>{
    return this.http.get<Student>(`${(this.BASE_URL)}${id}`)
  }

  public updateStudentDetails(id: number, student: Student) : Observable<Student>{
    return this.http.put<Student>(`${(this.BASE_URL)}${id}`, student)
  }

  public deleteStudent(id: number) : Observable<Student>{
    return this.http.delete<Student>(`${(this.BASE_URL)}${id}`)
  }
}
