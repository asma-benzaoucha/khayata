import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axiosInstance from "@/utils/axiosInstance"; // ✅ use our configured axios
import { Button } from "@/components/ui/button";
import { InputField } from "@/components/ui/inputField";
import { PasswordField } from "@/components/ui/passwordfield";
import { ArrowLeft } from "lucide-react";

export default function LoginPage() {
  const [errors, setErrors] = useState({ email: "", password: "" });
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [isLogging, setIsLogging] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();



  // --- Formulaire login ---
  const handleInputChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: "" }));
    }
  };

  const isFormValid = () => {
    return formData.email.trim() !== "" && formData.password.trim() !== "";
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isFormValid()) {
      setErrors({ email: "البريد مطلوب", password: "كلمة المرور مطلوبة" });
      return;
    }

    setIsLogging(true);
    setErrors({ email: "", password: "" });

    try {
      // ✅ Login request
      const response = await axiosInstance.post("/token/", formData);

      // ✅ Save tokens + user
      localStorage.setItem("accessToken", response.data.access);
      localStorage.setItem("refreshToken", response.data.refresh);
      localStorage.setItem("user", JSON.stringify(response.data.user));

      // ✅ Redirect by role
      const userRole = response.data.user.role;
      switch (userRole) {
        case "client":
          navigate("/client-dashboard");
          break;
        case "couturiere":
          navigate("/MesModels");
          break;
        case "dropshipper":
          navigate("/dropshipper-dashboard");
          break;
        case "affiliate":
          navigate("/AffiliateDashboard/CodePromo");
          break;
        case "admin":
          navigate("/admin-dashboard");
          break;
        default:
          navigate("/");
      }
    } catch (error) {
      console.error("Login failed:", error);

      if (error.response) {
        const data = error.response.data;
        const errorType = Array.isArray(data.error_type)
          ? data.error_type[0]
          : null;

        if (
          errorType === "couturiere_pending" ||
          errorType === "dropshipper_pending"
        ) {
          const role = errorType.split("_")[0];
          navigate(`/registration-${role}-success`, {
            state: {
              email: formData.email,
              role: role,
              message: `حسابك ك${
                role === "couturiere" ? "خياطة" : "موزع"
              } قيد المراجعة`,
            },
          });
          return;
        }
        if (
          errorType === "couturiere_refused" ||
          errorType === "dropshipper_refused"
        ) {
          const role = errorType.split("_")[0];
          navigate(`/registration-${role}-refused`, {
            state: {
              email: formData.email,
              role: role,
              message: `حسابك ك${
                role === "couturiere" ? "خياطة" : "موزع"
              } تم رفضه من طرف الإدارة.`,
            },
          });
          return;
        }

        const errorDetail = Array.isArray(data.detail)
          ? data.detail[0]
          : "حدث خطأ غير متوقع.";
        switch (errorType) {
          case "inactive_account":
            setErrors({
              email: "",
              password: "يرجى التحقق من بريدك الإلكتروني.",
            });
            break;
          case "account_disabled":
            setErrors({
              email: "",
              password: "تم تعطيل حسابك من قبل الإدارة...",
            });
            break;
          case "bad_email_or_password":
            setErrors({
              email: "",
              password: "البريد الإلكتروني أو كلمة المرور غير صحيحة.",
            });
            break;
          default:
            setErrors({ email: "", password: errorDetail });
        }
      } else {
        setErrors({
          email: "",
          password: error.request
            ? "خطأ في الاتصال بالخادم - تحقق من الاتصال"
            : "خطأ في إعداد الطلب",
        });
      }
    } finally {
      setIsLogging(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F4F3EF] flex flex-col items-center justify-start px-4 pt-8 pb-4 md:fixed md:inset-0">
      {/* Desktop Header (visible md and up) */}
      <div className="hidden md:flex relative w-full max-w-md justify-center items-center mb-4">
        <h2 className="text-[#E5B62B] text-2xl text-center amiri-bold">
          تسجيل الدخول
        </h2>
  
        {/* Back arrow (desktop - same as your original) */}
        <ArrowLeft
          onClick={() => navigate(-1)}
          className="absolute left-4 text-[#374151] w-5 h-5 cursor-pointer"
        />
  
        {/* Logo (desktop - fixed top-right like original) */}
        <div className="hidden md:block fixed top-4 right-0 z-50">
          <img
            src="/logo.png"
            alt="Logo"
            className="w-[8rem] max-w-full h-auto object-contain"
          />
        </div>
      </div>
  
      {/* Mobile Header (visible below md) - logo above, arrow left + centered title */}
      <div className="md:hidden w-full max-w-md flex flex-col items-center mb-4">
        <img
          src="/logo.png"
          alt="Logo"
          className="w-28 h-auto object-contain mb-4"
        />
  
        <div className="relative w-full flex justify-center items-center">
          <h2 className="text-[#E5B62B] text-xl text-center amiri-bold">
            تسجيل الدخول
          </h2>
  
          {/* Arrow placed on the left for mobile (keeps UX consistent with Arabic apps) */}
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
              <Link
                to="/forgot-password"
                className="text-[#4A66BD] text-sm underline cursor-pointer"
              >
                نسيت كلمة المرور؟
              </Link>
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
              <Link to="/signup" className="text-[#4A66BD] underline cursor-pointer">
                أنشئ حسابك الآن
              </Link>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
  
}

