import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {StudentDetailsComponent} from "./student-details/student-details.component";
import {StudentListComponent} from "./student-list/student-list.component";

const routes: Routes = [
  {path: '', component: StudentListComponent},
  {path: ':id', component: StudentDetailsComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
