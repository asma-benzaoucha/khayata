

// import { useState, useEffect } from "react";
// import { ArrowLeft } from "lucide-react";
// import { Button } from "@/components/ui/button";
// import { InputField } from "@/components/ui/inputField";
// import { Link, useNavigate } from "react-router-dom";
// import axios from "axios";

// export default function ForgotPassword() {
//   const [formData, setFormData] = useState({ email: "" });
//   const [errors, setErrors] = useState({});
//   const [isSending, setIsSending] = useState(false);
//   const navigate = useNavigate();

//   const handleInputChange = (field, value) => {
//     setFormData((prev) => ({ ...prev, [field]: value }));
//     if (errors[field]) {
//       setErrors((prev) => ({ ...prev, [field]: "" }));
//     }
//   };

//   useEffect(() => {
//     document.body.style.overflow = "hidden";
//     return () => {
//       document.body.style.overflow = "auto";
//     };
//   }, []);

//   const isFormValid = () => {
//     const email = formData.email.trim();
//     const errors = {};

//     const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//     const hasArabicChars = /[\u0600-\u06FF]/.test(email);

//     if (!email) {
//       errors.email = "البريد الإلكتروني مطلوب";
//     } else if (!emailRegex.test(email)) {
//       errors.email = "البريد الإلكتروني غير صحيح";
//     } else if (hasArabicChars) {
//       errors.email = "البريد الإلكتروني يجب أن يكون بالأحرف اللاتينية فقط";
//     }

//     if (Object.keys(errors).length > 0) {
//       setErrors(errors);
//       return false;
//     }

//     return true;
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (!isFormValid()) return;

//     setIsSending(true);
//     try {
//       const res = await axios.post("http://localhost:8000/api/forgot-password/", {
//         email: formData.email,
//       });

//       navigate("/verification", {
//         state: {
//           email: formData.email,
//           token: res.data.token,
//         },
//       });
//     } catch (err) {
//      // alert(err.response?.data?.detail || "حدث خطأ أثناء إرسال الرمز");
//       setError("حدث خطأ أثناء إرسال الرمز");

//     } finally {
//       setIsSending(false);
//     }
//   };

//   const handleBackToLogin = () => {
//     navigate("/login");
//   };

//   return (
//     <div className="fixed inset-0 bg-[#F4F3EF] flex flex-col items-center justify-start px-4 pt-8 pb-4">
//       <div className="relative w-full max-w-md flex justify-center items-center mb-4">
//         <h2 className="text-[#E5B62B] text-2xl text-center amiri-bold">نسيت كلمة المرور؟</h2>
//         <ArrowLeft
//           className="absolute left-4 text-[#374151] w-5 h-5 cursor-pointer"
//           onClick={handleBackToLogin}
//         />
//         <div className="fixed top-4 right-0 z-50">
//           <img
//             src="/logo.png"
//             alt="Logo"
//             className="w-[8rem] max-w-full h-auto object-contain"
//           />
//         </div>
//       </div>

//       <div className="bg-white rounded-t-3xl rounded-b-2xl shadow-md w-full max-w-xl h-[70vh] flex flex-col overflow-hidden">
//         <div className="overflow-y-auto px-6 py-6 flex-1" dir="rtl">
//           <form onSubmit={handleSubmit} className="space-y-6">
//             <p className="text-center text-[#374151] text-base leading-relaxed">
//               أدخل بريدك الإلكتروني وسنرسل لك رمزًا لإعادة تعيين كلمة المرور.
//             </p>

//             <div className="space-y-2 text-right">
//               <label className="text-sm text-[#374151] amiri-bold">
//                 البريد الإلكتروني:
//               </label>
//               <InputField
//                 label="البريد الإلكتروني:"
//                 type="email"
//                 placeholder="example@gmail.com"
//                 value={formData.email}
//                 onChange={(val) => handleInputChange("email", val)}
//                 error={errors.email}
//               />
//             </div>

//             <Button
//               type="submit"
//               className="w-full h-12 rounded-full text-white font-medium mt-2"
//               style={{ backgroundColor: "#E5B62B" }}
//               disabled={!formData.email || isSending}
//             >
//               {isSending ? "جارٍ الإرسال..." : "إرسال الرمز"}
//             </Button>

//             <div className="text-center">
//               <Link to="/login" className="text-[#4A66BD] text-sm underline cursor-pointer">
//                 العودة إلى تسجيل الدخول
//               </Link>
//             </div>
//           </form>
//         </div>
//       </div>
//     </div>
//   );
// }









import { useState, useEffect } from "react";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { InputField } from "@/components/ui/inputField";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

export default function ForgotPassword() {
  const [formData, setFormData] = useState({ email: "" });
  const [errors, setErrors] = useState({});
  const [isSending, setIsSending] = useState(false);
  const navigate = useNavigate();

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: "" }));
    }
  };

  useEffect(() => {
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = "auto";
    };
  }, []);

  const isFormValid = () => {
    const email = formData.email.trim();
    const newErrors = {};

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const hasArabicChars = /[\u0600-\u06FF]/.test(email);

    if (!email) {
      newErrors.email = "البريد الإلكتروني مطلوب";
    } else if (!emailRegex.test(email)) {
      newErrors.email = "البريد الإلكتروني غير صحيح";
    } else if (hasArabicChars) {
      newErrors.email = "البريد الإلكتروني يجب أن يكون بالأحرف اللاتينية فقط";
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isFormValid()) return;

    setIsSending(true);
    try {
      const res = await axios.post("http://localhost:8000/api/forgot-password/", {
        email: formData.email,
      });

      navigate("/verification", {
        state: {
          email: formData.email,
          token: res.data.token,
        },
      });
    } catch (err) {

      const detail = err.response?.data?.detail;

      if (typeof detail === "string") {
        setErrors(detail);
      } else if (Array.isArray(detail) && typeof detail[0] === "string") {
        setErrors(detail[0]);
      } else if (typeof detail === "object" && detail !== null && "string" in detail) {
        setErrors(detail.string);
      } else {
        setErrors("حدث خطأ أثناء إرسال الرمز");
        setErrors({ email: err.response?.data?.detail || "حدث خطأ أثناء إرسال الرمز" });

      }
    } finally {
      setIsSending(false);
    }
  };

  const handleBackToLogin = () => {
    navigate("/login");
  };

  // return (
  //   <div className="fixed inset-0 bg-[#F4F3EF] flex flex-col items-center justify-start px-4 pt-8 pb-4">
  //     <div className="relative w-full max-w-md flex justify-center items-center mb-4">
  //       <h2 className="text-[#E5B62B] text-2xl text-center amiri-bold">نسيت كلمة المرور؟</h2>
  //       <ArrowLeft onClick={() => navigate(-1)}
  //         className="absolute left-4 text-[#374151] w-5 h-5 cursor-pointer"
  //         // onClick={handleBackToLogin}
  //       />
  //       <div className="fixed top-4 right-0 z-50">
  //         <img
  //           src="/logo.png"
  //           alt="Logo"
  //           className="w-[8rem] max-w-full h-auto object-contain"
  //         />
  //       </div>
  //     </div>

  //     <div className="bg-white rounded-t-3xl rounded-b-2xl shadow-md w-full max-w-xl h-[70vh] flex flex-col overflow-hidden">
  //       <div className="overflow-y-auto px-6 py-6 flex-1" dir="rtl">
  //         <form onSubmit={handleSubmit} className="space-y-6">
  //           <p className="text-center text-[#374151] text-base leading-relaxed">
  //             أدخل بريدك الإلكتروني وسنرسل لك رمزًا لإعادة تعيين كلمة المرور.
  //           </p>

  //           <div className="space-y-2 text-right">
  //             <label className="text-sm text-[#374151] amiri-bold">
  //               البريد الإلكتروني:
  //             </label>
  //             <InputField
  //               type="text" // Important: avoid native HTML validation
  //               placeholder="example@gmail.com"
  //               value={formData.email}
  //               onChange={(val) => handleInputChange("email", val)}
  //               error={errors.email}
  //             />
  //           </div>

  //           <Button
  //             type="submit"
  //             className="w-full h-12 rounded-full text-white font-medium mt-2"
  //             style={{ backgroundColor: "#E5B62B" }}
  //             disabled={!formData.email || isSending}
  //           >
  //             {isSending ? "جارٍ الإرسال..." : "إرسال الرمز"}
  //           </Button>

  //           <div className="text-center">
  //             <Link to="/login" className="text-[#4A66BD] text-sm underline cursor-pointer">
  //               العودة إلى تسجيل الدخول
  //             </Link>
  //           </div>
  //         </form>
  //       </div>
  //     </div>
  //   </div>
  // );
  return (
    <div className="min-h-screen bg-[#F4F3EF] flex flex-col items-center justify-start px-4 pt-8 pb-4 md:fixed md:inset-0">
      {/* Desktop Header */}
      <div className="hidden md:flex relative w-full max-w-md justify-center items-center mb-4">
        <h2 className="text-[#E5B62B] text-2xl text-center amiri-bold">
          نسيت كلمة المرور؟
        </h2>
  
        {/* Back arrow (desktop - left) */}
        <ArrowLeft
          onClick={() => navigate(-1)}
          className="absolute left-4 text-[#374151] w-5 h-5 cursor-pointer"
        />
  
        {/* Logo (desktop - top right) */}
        <div className="hidden md:block fixed top-4 right-0 z-50">
          <img
            src="/logo.png"
            alt="Logo"
            className="w-[8rem] max-w-full h-auto object-contain"
          />
        </div>
      </div>
  
      {/* Mobile Header */}
      <div className="md:hidden w-full max-w-md flex flex-col items-center mb-4">
        <img
          src="/logo.png"
          alt="Logo"
          className="w-28 h-auto object-contain mb-4"
        />
  
        <div className="relative w-full flex justify-center items-center">
          <h2 className="text-[#E5B62B] text-xl text-center amiri-bold">
            نسيت كلمة المرور؟
          </h2>
          <ArrowLeft
            onClick={() => navigate(-1)}
            className="absolute left-4 text-[#374151] w-5 h-5 cursor-pointer"
          />
        </div>
      </div>
  
      {/* White Card */}
      <div
        className="
          bg-white rounded-2xl shadow-md w-full max-w-md
          md:max-w-xl md:rounded-t-3xl md:rounded-b-2xl md:h-[70vh] flex flex-col overflow-hidden
        "
      >
        <div className="overflow-y-auto px-6 py-6 flex-1" dir="rtl">
          <form onSubmit={handleSubmit} className="space-y-6">
            <p className="text-center text-[#374151] text-base leading-relaxed">
              أدخل بريدك الإلكتروني وسنرسل لك رمزًا لإعادة تعيين كلمة المرور.
            </p>
  
            <div className="space-y-2 text-right">
              <label className="text-sm text-[#374151] amiri-bold">
                البريد الإلكتروني:
              </label>
              <InputField
                type="text"
                placeholder="example@gmail.com"
                value={formData.email}
                onChange={(val) => handleInputChange("email", val)}
                error={errors.email}
              />
            </div>
  
            <Button
              type="submit"
              className="w-full h-12 rounded-full text-white font-medium mt-2"
              style={{ backgroundColor: "#E5B62B" }}
              disabled={!formData.email || isSending}
            >
              {isSending ? "جارٍ الإرسال..." : "إرسال الرمز"}
            </Button>
  
            <div className="text-center">
              <Link
                to="/login"
                className="text-[#4A66BD] text-sm underline cursor-pointer"
              >
                العودة إلى تسجيل الدخول
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
  
}

