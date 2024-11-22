import { Component } from "@angular/core";
import { FormGroup, FormControl } from "@angular/forms";
import { NgForm } from "@angular/forms";
import axios from "axios";
import { environment } from "src/environments/environment";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"],
})
export class AppComponent {
  title = "doctor-app";
  errorMessage = "";
  submissionInProgress = false;

  ngOnInit() {}

  async onSubmit(event: NgForm) {
    try {
      this.submissionInProgress = true;
      const { name, email, phone, date, message } = event.value;
      const res = await axios.post(`${environment.apiUrl}/appointment`, {
        name,
        email,
        phone,
        date,
        message,
      });

      if (res.status === 200) {
        alert("Appointment Booked!");
      }
      this.submissionInProgress = false;
    } catch (errorObj: any) {
      this.submissionInProgress = false;
      const { error } = errorObj.response.data;
      // alert(error);
      this.errorMessage = error;
    }
  }
}
