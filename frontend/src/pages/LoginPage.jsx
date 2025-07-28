import { useState, useEffect } from "react";
import { ArrowLeft } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function LoginPage() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  useEffect(() => {
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = "auto";
    };
  }, []);

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Login submitted:", formData);
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
              <label className="text-sm text-[#374151] amiri-bold">البريد الإلكتروني:</label>
              <Input
                type="email"
                placeholder="example@gmail.com"
                value={formData.email}
                onChange={(e) => handleInputChange("email", e.target.value)}
                className="w-full h-12 rounded-full border text-right pr-4 font-[Cairo] font-semibold"
                style={{ borderColor: "#73777A", backgroundColor: "#fff" }}
              />
            </div>

            <div className="space-y-2 text-right">
              <label className="text-sm text-[#374151] amiri-bold">كلمة المرور:</label>
              <Input
                type="password"
                placeholder="أدخل كلمة المرور"
                value={formData.password}
                onChange={(e) => handleInputChange("password", e.target.value)}
                className="w-full h-12 rounded-full border text-right pr-4 font-[Cairo] font-semibold"
                style={{ borderColor: "#73777A", backgroundColor: "#fff" }}
              />
            </div>

            <div className="text-right">
              <span className="text-[#4A66BD] text-sm underline cursor-pointer">
                نسيت كلمة المرور؟
              </span>
            </div>

            <Button
              type="submit"
              className="w-full h-12 rounded-full text-white font-medium mt-2"
              style={{ backgroundColor: "#E5B62B" }}
            >
              دخول
            </Button>

            <p className="text-center text-sm mt-4 text-[#374151]">
              ليس لديك حساب؟{" "}
              <span className="text-[#4A66BD] underline cursor-pointer">أنشئ حسابك الآن</span>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}
