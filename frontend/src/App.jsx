// import RegistrationSuccess from "./pages/user/registration-success-to-verified";
// import RegistrationCouturiere from "./pages/couturiere/registration-form-couturiere";
// import ForgotPassword from "./pages/user/forgot-password";
// import VerificationCode from "./pages/user/verificationCode";
// import PasswordSuccess from "./pages/user/PasswordSuccess";
// import ResetPassword from "./pages/user/ResetPassword";
// import LoginPage from "./pages/user/LoginPage";
// import Policy from "./pages/couturiere/policy";
// import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// import Demandes from "./pages/couturiere/demandes";
// import AffiliateCodePromoDashboard from "./pages/affiliate/mescodopromo"
// // import demandes from "./pages/couturiere/demandes"
// import MyAccount from "./pages/couturiere/moncompte"
// import MesModels from "./pages/couturiere/mesmodels";
// import AddNewModel from "./pages/couturiere/addmodel";
// import StatisticsPage from "./pages/affiliate/Statistics";
// import { ToastContainer } from "react-toastify";
// import "react-toastify/dist/ReactToastify.css";
// import DemandesOffresFassou from "./pages/couturiere/demandeoffrefassou"
// export default function App() {
//   return (
//     <>
//     <Router>
//       <Routes>
//         <Route path="/login" element={<LoginPage />} />
//         <Route path="/signup" element={<RegistrationCouturiere />} />
//         <Route path="/registration-success" element={<RegistrationSuccess />} />
//         <Route path="/forgot-password" element={<ForgotPassword />} />
//         <Route path="/verification" element={<VerificationCode />} />
//         <Route path="/reset-password" element={<ResetPassword />} />
//         <Route path="/password-success" element={<PasswordSuccess />} />
//         <Route path="/Policy" element={<Policy/>}/>

//         <Route path="/demandes" element={<Demandes/>}/>
    
//         <Route path="/MesModels" element={<MesModels/>}/>
//         <Route path="/AddNewModel" element={<AddNewModel/>}/>
//         <Route path="/moncompte" element={<MyAccount/>}/> 
//         <Route path="/AffiliateDashboard/CodePromo" element={<AffiliateCodePromoDashboard/>}/> 
//         <Route path="/AffiliateDashboard/Statistics" element={<StatisticsPage/>}/> 
//         <Route path="/DemandesOffresFassou" element={<DemandesOffresFassou/>}/>

//       </Routes>
//     </Router>
//     <ToastContainer
//   position="top-center"       // centré en haut, tu peux aussi "bottom-center"
//   autoClose={4000}
//   hideProgressBar
//   closeOnClick
//   draggable={false}
//   pauseOnHover
//   rtl={true}
//   toastStyle={{
//     backgroundColor: "#fff",       // fond blanc
//     color: "#333",                 // texte gris foncé
//     borderRadius: "16px",          // coins arrondis
//     boxShadow: "0 4px 20px rgba(0,0,0,0.15)", // ombre douce
//     padding: "20px",
//     fontSize: "15px",
//     fontFamily: "Tajawal, sans-serif",
//     textAlign: "center",
//     border: "1px solid #e5e5e5",
//   }}
// />

//     </>
//   );
// }


// App.jsx
import { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import { checkInitialAuth } from "@/utils/auth";

// 📦 Pages
import RegistrationSuccess from "./pages/user/registration-success-to-verified"; 
import RegistrationCouturiere from "./pages/couturiere/registration-form-couturiere";
import ForgotPassword from "./pages/user/forgot-password";
import VerificationCode from "./pages/user/verificationCode";
import PasswordSuccess from "./pages/user/PasswordSuccess";
import ResetPassword from "./pages/user/ResetPassword";
import LoginPage from "./pages/user/LoginPage";
import Policy from "./pages/couturiere/policy";
import Demandes from "./pages/couturiere/demandes";
import AffiliateCodePromoDashboard from "./pages/affiliate/mescodepromo";
import MyAccount from "./pages/couturiere/moncompte";
import AffiliateAccount from "./pages/affiliate/moncompte";
import MesModels from "./pages/couturiere/mesmodels";
import AddNewModel from "./pages/couturiere/addmodel";
import StatisticsPage from "./pages/affiliate/Statistics";
import DemandesOffresFassou from "./pages/couturiere/demandeoffrefassou";
import PolicyAffiliate from "./pages/affiliate/policy";
// 📦 UI
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

// ✅ Wrapper to handle auth check
function AppWrapper() {
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // useEffect(() => {
  //   const init = async () => {
  //     const isAuth = await checkInitialAuth();
  //     if (!isAuth) {
  //       navigate("/login");
  //     }
  //     setLoading(false);
  //   };
  //   init();
  // }, [navigate]);
  useEffect(() => {
    (async () => {
      const ok = await checkInitialAuth(location.pathname);
      if (!ok) {
        if (!["/login", "/signup", "/verification","/forgot-password","/reset-password","/registration-success", "/landing","/password-success"].includes(location.pathname)) {
          navigate("/login");
        }
      }
      setLoading(false);  // ✅ IMPORTANT
    })();
  }, [location.pathname]);
  
  return (
    <>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<RegistrationCouturiere />} />
        <Route path="/registration-success" element={<RegistrationSuccess />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/verification" element={<VerificationCode />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/password-success" element={<PasswordSuccess />} />
        <Route path="/Policy" element={<Policy />} />
        <Route path="/affiliate/policy" element={<PolicyAffiliate />} />
        {/* Private routes (require auth) */}
        <Route path="/demandes" element={<Demandes />} />
        <Route path="/MesModels" element={<MesModels />} />
        <Route path="/AddNewModel" element={<AddNewModel />} />
        <Route path="/couturiere/MyAccount" element={<MyAccount />} />
        <Route path="/affiliate/MyAccount" element={<AffiliateAccount />} />
        
        <Route path="/affiliateDashboard/codepromo" element={<AffiliateCodePromoDashboard />} />
        <Route path="/AffiliateDashboard/Statistics" element={<StatisticsPage />} />
        <Route path="/DemandesOffresFassou" element={<DemandesOffresFassou />} />
      </Routes>

      {/* ✅ Toast notifications */}
      <ToastContainer
        position="top-center"
        autoClose={4000}
        hideProgressBar
        closeOnClick
        draggable={false}
        pauseOnHover
        rtl={true}
        toastStyle={{
          backgroundColor: "#fff",
          color: "#333",
          borderRadius: "16px",
          boxShadow: "0 4px 20px rgba(0,0,0,0.15)",
          padding: "20px",
          fontSize: "15px",
          fontFamily: "Tajawal, sans-serif",
          textAlign: "center",
          border: "1px solid #e5e5e5",
        }}
      />
    </>
  );
}

// ✅ Main App with Router
export default function App() {
  return (
    <Router>
      <AppWrapper />
    </Router>
  );
}
