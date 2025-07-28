import { useState, useEffect } from "react"
import { ArrowLeft, Eye, EyeOff } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"

export default function RegistrationForm() {
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
    phone: "",
    address: "",
  })
  const [acceptTerms, setAcceptTerms] = useState(false)

  useEffect(() => {
    document.body.style.overflow = "hidden"
    return () => {
      document.body.style.overflow = "auto"
    }
  }, [])

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    console.log("Form submitted:", formData)
  }

  return (
    <div className="fixed inset-0 bg-[#F4F3EF] flex flex-col items-center justify-start px-4 pt-8 pb-4">
      {/* Header */}
      <div className="relative w-full max-w-md flex justify-center items-center mb-4">
        <h2 className="text-[#E5B62B] text-2xl text-center amiri-bold">تسجيل حساب خياطة</h2>
        <ArrowLeft className="absolute left-4 text-[#374151] w-5 h-5 cursor-pointer" />
        <div className="fixed top-4 right-0 z-50">

        <img src="\logo.png" alt="Logo"
             className="w-[8rem] max-w-full h-auto object-contain"
             />

        </div>
      </div>

      {/* White Card */}
      <div className="bg-white rounded-t-3xl rounded-b-2xl shadow-md w-full max-w-xl h-[90vh] flex flex-col overflow-hidden">
        <div className="overflow-y-auto px-6 py-6 flex-1" dir="rtl">
          <form onSubmit={handleSubmit} className="space-y-4">
            <InputField
              label="الاسم الكامل:"
              placeholder="ادخل الاسم الكامل"
              value={formData.fullName}
              onChange={(val) => handleInputChange("fullName", val)}
            />

            <InputField
              label="البريد الإلكتروني:"
              type="email"
              placeholder="example@gmail.com"
              value={formData.email}
              onChange={(val) => handleInputChange("email", val)}
            />

            <PasswordField
              label="كلمة المرور:"
              placeholder="ادخل كلمة المرور"
              value={formData.password}
              show={showPassword}
              toggleShow={() => setShowPassword((prev) => !prev)}
              onChange={(val) => handleInputChange("password", val)}
            />

            <PasswordField
              label="تأكيد كلمة المرور:"
              placeholder="أدخل كلمة المرور لتأكيدها"
              value={formData.confirmPassword}
              show={showConfirmPassword}
              toggleShow={() => setShowConfirmPassword((prev) => !prev)}
              onChange={(val) => handleInputChange("confirmPassword", val)}
            />

            <InputField
              label="رقم الهاتف:"
              type="tel"
              placeholder="0123456789"
              value={formData.phone}
              onChange={(val) => handleInputChange("phone", val)}
            />

            <InputField
              label="عنوان الاقامة:"
              placeholder="الشارع، المدينة، الولاية"
              value={formData.address}
              onChange={(val) => handleInputChange("address", val)}
            />

            <Button
              type="button"
              variant="outline"
              className="w-full h-12 rounded-full border border-[#E5B62B] text-[#E5B62B]"
            >
              اختر ملفات لإثبات مهاراتك
            </Button>

            <div className="flex items-center  mt-4 gap-2">
              <Checkbox
                checked={acceptTerms}
                onCheckedChange={(c) => setAcceptTerms(c)}
                className="data-[state=checked]:bg-[#E5B62B] data-[state=checked]:border-[#E5B62B]"
              />
              <label className="text-sm text-right text-[#374151] leading-5">
                أوافق على{" "}
                <span className="text-[#E5B62B] underline cursor-pointer">شروط الاستخدام</span>
                ,{" "}
                <span className="text-[#E5B62B] underline cursor-pointer">
                  سياسة التسجيل الخاصة بالخياطات
                </span>
              </label>
            </div>

            <Button
              type="submit"
              disabled={!acceptTerms}
              className="w-full h-12 rounded-full text-white font-medium mt-4 disabled:opacity-50"
              style={{ backgroundColor: "#E5B62B" }}
            >
              إنشاء حساب
            </Button>

            <p className="text-center text-sm mt-4 text-[#374151]">
              هل لديك حساب بالفعل؟{" "}
              <span className="text-[#4A66BD] underline cursor-pointer">تسجيل الدخول</span>
            </p>
          </form>
        </div>
      </div>
    </div>
  )
}

// Reusable Components

function InputField({ label, type = "text", placeholder, value, onChange }) {
  return (
    <div className="space-y-2 text-right">
      <label className="text-sm text-[#374151] amiri-bold">{label}</label>
      <Input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full h-12 rounded-full border text-right pr-4 font-[Cairo] font-semibold"
        style={{ borderColor: "#73777A", backgroundColor: "#fff" }}
      />
    </div>
  )
}

function PasswordField({ label, placeholder, value, show, toggleShow, onChange }) {
  return (
    <div className="space-y-2 text-right">
      <label className="text-sm text-[#374151] amiri-bold">{label}</label>
      <div className="relative">
        <Input
          type={show ? "text" : "password"}
          placeholder={placeholder}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="w-full h-12 rounded-full border text-right pr-4 pl-12 font-[Cairo] font-semibold"
          style={{ borderColor: "#73777A", backgroundColor: "#fff" }}
        />
        <button
          type="button"
          onClick={toggleShow}
          className="absolute left-4 top-1/2 transform -translate-y-1/2"
        >
          {show ? (
            <EyeOff className="h-5 w-5 text-[#DADAD7]" />
          ) : (
            <Eye className="h-5 w-5 text-[#DADAD7]" />
          )}
        </button>
      </div>
    </div>
  )
}
