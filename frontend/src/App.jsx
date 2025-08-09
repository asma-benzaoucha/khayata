import RegistrationSuccess from "./pages/user/registration-success-to-verified";
import RegistrationCouturiere from "./pages/user/registration-form-couturiere";
import ForgotPassword from "./pages/user/forgot-password";
import VerificationCode from "./pages/user/verificationCode";
import PasswordSuccess from "./pages/user/PasswordSuccess";
import ResetPassword from "./pages/user/ResetPassword";
import LoginPage from "./pages/user/LoginPage";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';



export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<RegistrationCouturiere />} />
        
        <Route path="/registration-success" element={<RegistrationSuccess />} />

        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/verification" element={<VerificationCode />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/password-success" element={<PasswordSuccess />} />
      </Routes>
    </Router>
  );
}
