import { useEffect } from "react";
import { ArrowLeft, CheckCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import {Link ,useNavigate} from "react-router-dom";
export default function PasswordSuccess() {
  const handleBackToLogin = () => {
    console.log("Navigate to login");
  };

  useEffect(() => {
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = "auto";
    };
  }, []);

  // return (
  //   <div className="fixed inset-0 bg-[#F4F3EF] flex flex-col items-center justify-start px-4 pt-8 pb-4">
  //     {/* Header */}
  //     <div className="relative w-full max-w-md flex justify-center items-center mb-4">
  //       <h2 className="text-[#E5B62B] text-2xl text-center amiri-bold">
  //         تم حفظ كلمة المرور بنجاح
  //       </h2>
  //       <ArrowLeft
  //         className="absolute left-4 text-[#374151] w-5 h-5 cursor-pointer"
  //         onClick={() => navigate(-1)}        />
  //       <div className="fixed top-4 right-0 z-50">
  //         <img
  //           src="/logo.png"
  //           alt="Logo"
  //           className="w-[8rem] max-w-full h-auto object-contain"
  //         />
  //       </div>
  //     </div>

  //     {/* Content Card */}
  //     <div className="bg-white rounded-t-3xl rounded-b-2xl shadow-md w-full max-w-xl h-[70vh] flex flex-col overflow-hidden">
  //       <div className="overflow-y-auto px-6 py-6 flex-1 flex flex-col items-center justify-center space-y-8 text-center" dir="rtl">
  //         {/* Success Icon */}
  //         <CheckCircle className="h-16 w-16 text-[#10B981]" />

  //         {/* Message */}
  //         <p className="text-lg leading-relaxed text-[#374151] font-[Cairo] font-medium">
  //           يمكنك الآن تسجيل الدخول باستخدام كلمة المرور الجديدة.
  //         </p>

  //         {/* Back to Login Button */}
  //         <Button
  //           onClick={handleBackToLogin}
  //           className="w-full h-12 rounded-full text-white font-medium"
  //           style={{ backgroundColor: "#E5B62B" }}
  //         >
  //           <Link to="/login">
  //           العودة إلى تسجيل الدخول

  //           </Link>
  //         </Button>
  //       </div>
  //     </div>
  //   </div>
  // );


  return (
    <div className="fixed inset-0 bg-[#F4F3EF] flex flex-col items-center justify-start px-4 pt-8 pb-4">
      {/* --- HEADER DESKTOP --- */}
      <div className="hidden md:flex relative w-full max-w-md justify-center items-center mb-4">
        <h2 className="text-[#E5B62B] text-2xl text-center amiri-bold">
          تم حفظ كلمة المرور بنجاح
        </h2>
        <ArrowLeft
          onClick={() => navigate(-1)}
          className="absolute left-4 text-[#374151] w-5 h-5 cursor-pointer"
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
        {/* Logo */}
        <div className="w-full flex justify-center mb-2">
          <img
            src="/logo.png"
            alt="Logo"
            className="w-[8rem] max-w-full h-auto object-contain"
          />
        </div>

        {/* Arrow + Title */}
        <div className="relative w-full max-w-md flex items-center justify-center mb-4">
          <ArrowLeft
            onClick={() => navigate(-1)}
            className="absolute left-4 text-[#374151] w-5 h-5 cursor-pointer"
          />
          <h2 className="text-[#E5B62B] text-2xl text-center amiri-bold">
            تم حفظ كلمة المرور بنجاح
          </h2>
        </div>
      </div>

      {/* --- CONTENT CARD --- */}
      <div className="bg-white rounded-t-3xl rounded-b-2xl shadow-md w-full max-w-xl h-[70vh] flex flex-col overflow-hidden">
        <div
          className="overflow-y-auto px-6 py-6 flex-1 flex flex-col items-center justify-center space-y-8 text-center"
          dir="rtl"
        >
          {/* Success Icon */}
          <CheckCircle className="h-16 w-16 text-[#10B981]" />

          {/* Message */}
          <p className="text-lg leading-relaxed text-[#374151] font-[Cairo] font-medium">
            يمكنك الآن تسجيل الدخول باستخدام كلمة المرور الجديدة.
          </p>

          {/* Back to Login Button */}
          <Button
            className="w-full h-12 rounded-full text-white font-medium"
            style={{ backgroundColor: "#E5B62B" }}
          >
            <Link to="/login" className="block w-full h-full">
              العودة إلى تسجيل الدخول
            </Link>
          </Button>
        </div>
      </div>
    </div>
  );  
}
