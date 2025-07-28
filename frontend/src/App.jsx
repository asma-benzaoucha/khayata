import { useState } from "react"
import VerificationCode from "./pages/verificationCode"
import PasswordSuccess from "./pages/PasswordSuccess"
import RegistrationSuccess from "./pages/registration-success-to-verified"
import RegistrationCouturiere from "./pages/registration-form-couturiere"
import ForgotPassword from "./pages/forgot-password"
import ResetPassword from "./pages/ResetPassword"
import LoginPage from "./pages/LoginPage"
import { Button } from "./components/ui/button"
import "./App.css"

export default function App() {
  const [currentScreen, setCurrentScreen] = useState("login")

  const screens = {
    login: <LoginPage />,
    verification: <VerificationCode />,
    passwordSuccess: <PasswordSuccess />,
    registrationSuccess: <RegistrationSuccess />,
    forgotPassword: <ForgotPassword />,
    RegistrationCouturiere :<RegistrationCouturiere/>,
    ResetPassword:<ResetPassword/>
  }

  return (
    <div>
      {/* Navigation for demo purposes */}
      <div className="fixed top-4 left-4 z-50 flex gap-2 flex-wrap">
        <Button
          size="sm"
          variant={currentScreen === "login" ? "default" : "outline"}
          onClick={() => setCurrentScreen("login")}
        >
          Login
        </Button>
        <Button
          size="sm"
          variant={currentScreen === "registrationSuccess" ? "default" : "outline"}
          onClick={() => setCurrentScreen("registrationSuccess")}
        >
          RegistrationSucess
        </Button>
        <Button
          size="sm"
          variant={currentScreen === "" ? "default" : "outline"}
          onClick={() => setCurrentScreen("RegistrationCouturiere")}        >
          RegistrationCouturiere
        </Button>
        <Button
          size="sm"
          variant={currentScreen === "" ? "default" : "outline"}
          onClick={() => setCurrentScreen("ResetPassword")}        >
          ResetPassword
        </Button>
        
        <Button
          size="sm"
          variant={currentScreen === "forgotPassword" ? "default" : "outline"}
          onClick={() => setCurrentScreen("forgotPassword")}
        >
          Forgot Password
        </Button>
        <Button
          size="sm"
          variant={currentScreen === "verification" ? "default" : "outline"}
          onClick={() => setCurrentScreen("verification")}
        >
          Verification
        </Button>       
        <Button
          size="sm"
          variant={currentScreen === "passwordSuccess" ? "default" : "outline"}
          onClick={() => setCurrentScreen("passwordSuccess")}
        >
          passwordSuccess
        </Button>
      </div>
      {screens[currentScreen]}
    </div>
  )
}
