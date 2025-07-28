import { useState, useEffect } from "react";
import { ArrowLeft, Eye, EyeOff } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function ResetPassword() {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  useEffect(() => {
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = "auto";
    };
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Reset password:", { password, confirmPassword });
  };

  const handleBack = () => {
    console.log("Back to previous screen");
  };

  return (
    <div className="fixed inset-0 bg-[#F4F3EF] flex flex-col items-center justify-start px-4 pt-8 pb-4">
      {/* Header */}
      <div className="relative w-full max-w-md flex justify-center items-center mb-4">
        <h2 className="text-[#E5B62B] text-2xl text-center amiri-bold">
          إعادة تعيين كلمة المرور
        </h2>
        <ArrowLeft
          className="absolute left-4 text-[#374151] w-5 h-5 cursor-pointer"
          onClick={handleBack}
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
      <div className="bg-white rounded-t-3xl rounded-b-2xl shadow-md w-full max-w-xl h-[75vh] flex flex-col overflow-hidden">
        <div className="overflow-y-auto px-6 py-6 flex-1" dir="rtl">
          <form onSubmit={handleSubmit} className="space-y-6 text-right font-[Cairo]">
            {/* Instruction */}
            <p className="text-base text-[#374151] text-center">
              الرجاء إدخال كلمة مرور جديدة لحسابك.
            </p>

            {/* Password Field */}
            <div className="space-y-2">
              <label className="text-sm text-[#374151] amiri-bold">
                كلمة المرور:
              </label>
              <div className="relative">
                <Input
                  type={showPassword ? "text" : "password"}
                  placeholder="أدخل كلمة المرور"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full h-12 rounded-full border pr-4 pl-12 text-right font-semibold"
                  style={{ borderColor: "#73777A", backgroundColor: "#fff" }}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((prev) => !prev)}
                  className="absolute left-4 top-1/2 transform -translate-y-1/2"
                >
                  {showPassword ? (
                    <EyeOff className="h-5 w-5 text-[#DADAD7]" />
                  ) : (
                    <Eye className="h-5 w-5 text-[#DADAD7]" />
                  )}
                </button>
              </div>
            </div>

            {/* Confirm Password Field */}
            <div className="space-y-2">
              <label className="text-sm text-[#374151] amiri-bold">
                تأكيد كلمة المرور:
              </label>
              <div className="relative">
                <Input
                  type={showConfirmPassword ? "text" : "password"}
                  placeholder="أدخل كلمة المرور لتأكيدها"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full h-12 rounded-full border pr-4 pl-12 text-right font-semibold"
                  style={{ borderColor: "#73777A", backgroundColor: "#fff" }}
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword((prev) => !prev)}
                  className="absolute left-4 top-1/2 transform -translate-y-1/2"
                >
                  {showConfirmPassword ? (
                    <EyeOff className="h-5 w-5 text-[#DADAD7]" />
                  ) : (
                    <Eye className="h-5 w-5 text-[#DADAD7]" />
                  )}
                </button>
              </div>
            </div>

            {/* Save Button */}
            <Button
              type="submit"
              className="w-full h-12 rounded-full text-white font-medium mt-4"
              style={{ backgroundColor: "#E5B62B" }}
              disabled={!password || !confirmPassword}
            >
              حفظ
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
