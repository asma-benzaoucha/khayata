import RegistrationSuccess from "./pages/user/registration-success-to-verified";
import RegistrationCouturiere from "./pages/user/registration-form-couturiere";
import ForgotPassword from "./pages/user/forgot-password";
import VerificationCode from "./pages/user/verificationCode";
import PasswordSuccess from "./pages/user/PasswordSuccess";
import ResetPassword from "./pages/user/ResetPassword";
import LoginPage from "./pages/user/LoginPage";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landingpage from './pages/client/Landingpage';
import ShoppingPage from './pages/client/ShoppingPage'
import FormAcheter from './pages/client/FormAcheterPage'
import ModelSpecialPage from "./pages/client/ModelSpecialPage";
import CompteclientPage from "./pages/client/CompteclientPage";
import Talabiyati from "./pages/client/Talabiyati";
import Popupimages from "./components/generalComponents/Popupimages";
import Test from "./components/generalComponents/test";
import LoginClient from "./pages/client/LoginClient";
import RegistrationClient from "./pages/client/RegistrationClient";


export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/loginClient" element={<LoginClient />} />
        <Route path="/registerclient" element={<RegistrationClient />} />

        <Route path="/signup" element={<RegistrationCouturiere />} />
        
        <Route path="/registration-success" element={<RegistrationSuccess />} />

        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/verification" element={<VerificationCode />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/password-success" element={<PasswordSuccess />} />

        <Route path="/" element={<Landingpage />} />
        <Route path="/shopping" element={<ShoppingPage />} />
        <Route path="/shopping/acheter" element={<FormAcheter />} />
        <Route path="/special" element={<ModelSpecialPage />} />
        <Route path="/compte" element={<CompteclientPage />} />
        <Route path="/mycommands" element={<Talabiyati />} />
        <Route path="/images" element={<Test />} />

      </Routes>
    </Router>
  );
}
