import React from "react";
import { ArrowLeft, XCircle } from "lucide-react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import { Button } from "@/components/ui/button";

export default function RegistrationRefuse() {
  const navigate = useNavigate();
  const location = useLocation();

  // Récupération des données passées via navigate(..., { state })
  const { email, role, message } = location.state || {};

  const getRoleText = () => {
    switch (role) {
      case "couturiere":
        return "خياطة";
      case "dropshipper":
        return "موزع";
      default:
        return "مستخدم";
    }
  };

  const handleBackToHome = () => {
    navigate("/");
  };

  return (
    <div className="fixed inset-0 bg-[#F4F3EF] flex flex-col items-center justify-start px-4 pt-8 pb-4">
      {/* --- HEADER DESKTOP --- */}
      <div className="hidden md:flex relative w-full max-w-md justify-center items-center mb-4">
        <h2 className="text-[#E5B62B] text-2xl text-center amiri-bold">
          عذراً، لم يتم قبول تسجيلك
        </h2>
        <ArrowLeft
          className="absolute left-4 text-[#374151] w-5 h-5 cursor-pointer"
          onClick={() => navigate(-1)}
        />
        <div className="fixed top-4 right-0 z-50">
          <img
            src="/logo.png"
            alt="Logo"
            className="w-[8rem] max-w-full h-auto object-contain"
          />
        </div>
      </div>

      {/* --- HEADER MOBILE --- */}
      <div className="md:hidden w-full">
        <div className="w-full flex justify-center mb-2">
          <img
            src="/logo.png"
            alt="Logo"
            className="w-[8rem] max-w-full h-auto object-contain"
          />
        </div>

        <div className="relative w-full max-w-md flex items-center justify-center mb-4">
          <ArrowLeft
            onClick={() => navigate(-1)}
            className="absolute left-4 text-[#374151] w-5 h-5 cursor-pointer"
          />
          <h2 className="text-[#E5B62B] text-2xl text-center amiri-bold">
            عذراً، لم يتم قبول تسجيلك
          </h2>
        </div>
      </div>

      {/* --- CONTENT CARD --- */}
      <div className="bg-white rounded-t-3xl rounded-b-2xl shadow-md w-full max-w-xl h-[70vh] flex flex-col overflow-hidden">
        <div
          className="overflow-y-auto px-6 py-6 flex-1 flex flex-col items-center justify-center space-y-8 text-center"
          dir="rtl"
        >
          <XCircle className="h-16 w-16 text-red-500 animate-pulse" />

          <div className="space-y-4">
            <p className="text-lg font-[Cairo] font-medium text-[#182544]">
              {message ||
                `تم رفض طلب تسجيلك كـ ${getRoleText()} من قبل الإدارة.`}
            </p>
            <p className="text-[#374151]">
              نعتذر منك، لقد تمت مراجعة معلوماتك وقررت الإدارة عدم قبول تسجيلك
              {role && ` كـ ${getRoleText()}`} .
            </p>
            {email && (
              <p className="text-sm text-gray-600">
                يمكنك متابعة بريدك الإلكتروني:{" "}
                <span className="font-bold">{email}</span>
              </p>
            )}
            <p className="text-sm text-gray-600">
              لمزيد من التفاصيل يرجى التواصل مع الدعم.
            </p>
          </div>

          <Button
            onClick={handleBackToHome}
            className="w-full h-12 rounded-full text-white font-medium hover:bg-[#d4a41e]"
            style={{ backgroundColor: "#E5B62B" }}
          >
            <Link to="/">العودة إلى الرئيسية</Link>
          </Button>
        </div>
      </div>
    </div>
  );
}
