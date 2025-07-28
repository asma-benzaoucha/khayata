import { useState, useEffect } from "react";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");

  useEffect(() => {
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = "auto";
    };
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Reset password for:", email);
  };

  const handleBackToLogin = () => {
    console.log("Navigate back to login");
  };

  return (
    <div className="fixed inset-0 bg-[#F4F3EF] flex flex-col items-center justify-start px-4 pt-8 pb-4">
      {/* Header */}
      <div className="relative w-full max-w-md flex justify-center items-center mb-4">
        <h2 className="text-[#E5B62B] text-2xl text-center amiri-bold">نسيت كلمة المرور؟</h2>
        <ArrowLeft
          className="absolute left-4 text-[#374151] w-5 h-5 cursor-pointer"
          onClick={handleBackToLogin}
        />
        <div className="fixed top-4 right-0 z-50">
          <img
            src="/logo.png"
            alt="Logo"
            className="w-[8rem] max-w-full h-auto object-contain"
          />
        </div>
      </div>

      {/* Card */}
      <div className="bg-white rounded-t-3xl rounded-b-2xl shadow-md w-full max-w-xl h-[70vh] flex flex-col overflow-hidden">
        <div className="overflow-y-auto px-6 py-6 flex-1" dir="rtl">
          <form onSubmit={handleSubmit} className="space-y-6">
            <p className="text-center text-[#374151] text-base leading-relaxed">
              أدخل بريدك الإلكتروني وسنرسل لك رمزًا لإعادة تعيين كلمة المرور.
            </p>

            <div className="space-y-2 text-right">
              <label className="text-sm text-[#374151] amiri-bold">
                البريد الإلكتروني:
              </label>
              <Input
                type="email"
                placeholder="example@gmail.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full h-12 rounded-full border text-right pr-4 font-[Cairo] font-semibold"
                style={{ borderColor: "#73777A", backgroundColor: "#fff" }}
                required
              />
            </div>

            <Button
              type="submit"
              className="w-full h-12 rounded-full text-white font-medium mt-2"
              style={{ backgroundColor: "#E5B62B" }}
              disabled={!email}
            >
              إرسال الرمز
            </Button>

            <div className="text-center">
              <button
                type="button"
                onClick={handleBackToLogin}
                className="text-[#4A66BD] text-sm underline cursor-pointer"
              >
                العودة إلى تسجيل الدخول
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
