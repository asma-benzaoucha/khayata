import { useState, useEffect } from "react";
import { ArrowLeft } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { InputField } from "@/components/ui/inputField";
import { PasswordField } from "@/components/ui/passwordfield";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

export default function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState({ email: "", password: "" });
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [isLogging, setIsLogging] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = "auto";
    };
  }, []);

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    // Clear errors when user starts typing
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: "" }));
    }
  };

  const isFormValid = () => {
    return formData.email.trim() !== "" && formData.password.trim() !== "";
  };
// ... (imports restent identiques)

const handleSubmit = async (e) => {
  e.preventDefault();

  if (!isFormValid()) {
    setErrors({ email: "البريد مطلوب", password: "كلمة المرور مطلوبة" });
    return;
  }

  setIsLogging(true);
  setErrors({ email: "", password: "" });

  try {
    const response = await axios.post("http://127.0.0.1:8000/api/token/", formData, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 10000,
    });

    localStorage.setItem("accessToken", response.data.access);
    localStorage.setItem("refreshToken", response.data.refresh);
    localStorage.setItem("user", JSON.stringify(response.data.user));

    // Redirection selon le rôle
    const userRole = response.data.user.role;
    switch (userRole) {
      case "client": navigate("/client-dashboard"); break;
      case "couturiere": navigate("/couturiere-dashboard"); break;
      case "dropshipper": navigate("/dropshipper-dashboard"); break;
      default: navigate("/");
    }

  } catch (error) {
    console.error("Login failed:", error);

    if (error.response) {
      const data = error.response.data;
      const errorType = Array.isArray(data.error_type) ? data.error_type[0] : null;

      // Gestion unifiée des comptes en attente
      if (errorType === "couturiere_pending" || errorType === "dropshipper_pending") {
        const role = errorType.split('_')[0]; // "couturiere" ou "dropshipper"
        navigate("/registration-success", {
          state: {
            email: formData.email,
            role: role,
            message: `حسابك ك${role === "couturiere" ? "خياطة" : "موزع"} قيد المراجعة`
          }
        });
        return;
      }

      // Gestion des autres erreurs
      const errorDetail = Array.isArray(data.detail) ? data.detail[0] : "حدث خطأ غير متوقع.";
      switch (errorType) {
        case "inactive_account":
          setErrors({ email: "", password: "يرجى التحقق من بريدك الإلكتروني." });
          break;
        case "account_disabled":
          setErrors({ email: "", password: "تم تعطيل حسابك من قبل الإدارة..." });
          break;
        case "bad_email_or_password":
          setErrors({ email: "", password: "البريد الإلكتروني أو كلمة المرور غير صحيحة." });
          break;
        default:
          setErrors({ email: "", password: errorDetail });
      }
    } else {
      setErrors({ 
        email: "", 
        password: error.request 
          ? "خطأ في الاتصال بالخادم - تحقق من الاتصال" 
          : "خطأ في إعداد الطلب" 
      });
    }
  } finally {
    setIsLogging(false);
  }
};

  return (
    <div className="fixed inset-0 bg-[#F4F3EF] flex flex-col items-center justify-start px-4 pt-8 pb-4">
      {/* Header */}
      <div className="relative w-full max-w-md flex justify-center items-center mb-4">
        <h2 className="text-[#E5B62B] text-2xl text-center amiri-bold">تسجيل الدخول</h2>
        <ArrowLeft className="absolute left-4 text-[#374151] w-5 h-5 cursor-pointer" />
        <div className="fixed top-4 right-0 z-50">
          <img
            src="/logo.png"
            alt="Logo"
            className="w-[8rem] max-w-full h-auto object-contain"
          />
        </div>
      </div>
      {/* White Card */}
      <div className="bg-white rounded-t-3xl rounded-b-2xl shadow-md w-full max-w-xl h-[70vh] flex flex-col overflow-hidden">
        <div className="overflow-y-auto px-6 py-6 flex-1" dir="rtl">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2 text-right">
              <InputField
                label="البريد الإلكتروني:"
                type="email"
                placeholder="example@gmail.com"
                value={formData.email}
                onChange={(val) => handleInputChange("email", val)}
                error={errors.email}
              />
              <PasswordField
                label="كلمة المرور:"
                placeholder="ادخل كلمة المرور"
                value={formData.password}
                show={showPassword}
                toggleShow={() => setShowPassword((prev) => !prev)}
                onChange={(val) => handleInputChange("password", val)}
                error={errors.password}
              />
            </div>
            <div className="text-right">
              <span className="text-[#4A66BD] text-sm underline cursor-pointer">
                <Link to="/forgot-password">
                نسيت كلمة المرور؟ 
                </Link>
              </span>
            </div>
            <Button
              type="submit"
              disabled={!isFormValid() || isLogging}
              className="w-full h-12 rounded-full text-white font-medium mt-4 disabled:opacity-50"
              style={{ backgroundColor: "#E5B62B" }}
            >
              {isLogging ? "جاري الدخول..." : "دخول"}
            </Button>
            <p className="text-center text-sm mt-4 text-[#374151]">
              ليس لديك حساب؟{" "}
              <span className="text-[#4A66BD] underline cursor-pointer">
                <Link to="/signup">
                أنشئ حسابك الآن
                </Link>
              </span>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}

