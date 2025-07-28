import { useState, useEffect } from "react";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function VerificationCode() {
  const [code, setCode] = useState(["", "", "", "", "", ""]);
  const [timeLeft, setTimeLeft] = useState(30);
  const [canResend, setCanResend] = useState(false);

  useEffect(() => {
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = "auto";
    };
  }, []);

  useEffect(() => {
    if (timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else {
      setCanResend(true);
    }
  }, [timeLeft]);

  const handleCodeChange = (index, value) => {
    if (value.length <= 1 && /^[0-9]*$/.test(value)) {
      const newCode = [...code];
      newCode[index] = value;
      setCode(newCode);
      if (value && index < 5) {
        const nextInput = document.getElementById(`code-${index + 1}`);
        nextInput?.focus();
      }
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Verification code:", code.join(""));
  };

  const handleResend = () => {
    setTimeLeft(30);
    setCanResend(false);
    setCode(["", "", "", "", "", ""]);
    console.log("Resend code");
  };

  const handleBack = () => {
    console.log("Back to previous screen");
  };

  return (
    <div className="fixed inset-0 bg-[#F4F3EF] flex flex-col items-center justify-start px-4 pt-8 pb-4">
      {/* Header */}
      <div className="relative w-full max-w-md flex justify-center items-center mb-4">
        <h2 className="text-[#E5B62B] text-2xl text-center amiri-bold">
          تأكيد الرمز
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
      <div className="bg-white rounded-t-3xl rounded-b-2xl shadow-md w-full max-w-xl h-[80vh] flex flex-col overflow-hidden">
        <div className="overflow-y-auto px-6 py-6 flex-1" dir="rtl">
          <form onSubmit={handleSubmit} className="space-y-8 text-center">
            {/* Instruction */}
            <p className="text-base text-[#374151] font-[Cairo]">
              لقد تم إرسال الرمز، يرجى إدخاله أدناه.
            </p>

            {/* Code Input */}
            <div className="flex justify-center gap-3">
              {code.map((digit, index) => (
                <input
                  key={index}
                  id={`code-${index}`}
                  type="text"
                  maxLength={1}
                  inputMode="numeric"
                  value={digit}
                  onChange={(e) => handleCodeChange(index, e.target.value)}
                  className="w-12 h-12 text-center text-xl font-bold rounded-lg border-2 focus:outline-none focus:ring-2"
                  style={{
                    borderColor: digit ? "#E5B62B" : "#DADAD7",
                    backgroundColor: "#F9F9F9",
                    color: "#374151",
                  }}
                />
              ))}
            </div>

            {/* Timer */}
            <p className="text-sm text-[#374151] font-[Cairo]">
              ينتهي الرمز خلال {timeLeft} ثانية
            </p>

            {/* Confirm Button */}
            <Button
              type="submit"
              className="w-full h-12 rounded-full text-white font-medium"
              style={{ backgroundColor: "#E5B62B" }}
              disabled={code.some((digit) => !digit)}
            >
              تأكيد الرمز
            </Button>

            {/* Resend */}
            <div className="text-center">
              <button
                type="button"
                onClick={handleResend}
                disabled={!canResend}
                className={`text-base underline transition-all font-[Cairo] ${
                  canResend
                    ? "text-[#3B82F6] cursor-pointer"
                    : "opacity-50 cursor-not-allowed text-[#3B82F6]"
                }`}
              >
                لم يصلك الرمز؟ أعد الإرسال
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
