import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'aif-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {

  public loginForm: FormGroup;
  public isPasswordHidden: boolean = true;

  constructor(private fb: FormBuilder, private router: Router) {
    this.loginForm = this.createLoginForm();
  }

  public get typePasswordField(): string {
    return this.isPasswordHidden ? 'password' : 'text';
  }

  public get iconPassword(): string {
    return this.isPasswordHidden ? 'eye-outline' : 'eye-off-outline';
  }

  public login(): void {
    this.router.navigate(['/shops']);
  }

  public togglePassword(): void {
    this.isPasswordHidden = !this.isPasswordHidden;
  }

  private createLoginForm(): FormGroup {
    return this.fb.group({
      login: '',
      password: ''
    });
  }
}
