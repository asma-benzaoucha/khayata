import { useEffect } from "react"
import { CheckCircle, ArrowLeft } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function RegistrationSuccess() {
  useEffect(() => {
    document.body.style.overflow = "hidden"
    return () => {
      document.body.style.overflow = "auto"
    }
  }, [])

  const handleBackToHome = () => {
    console.log("Navigate to home")
  }

  return (
    <div className="fixed inset-0 bg-[#F4F3EF] flex flex-col items-center justify-start px-4 pt-8 pb-4">
      {/* Header */}
      <div className="relative w-full max-w-md flex justify-center items-center mb-4">
        <h2 className="text-[#E5B62B] text-2xl text-center amiri-bold">شكراً لتسجيلك!</h2>
        <ArrowLeft
          className="absolute left-4 text-[#374151] w-5 h-5 cursor-pointer"
          onClick={handleBackToHome}
        />
        <div className="fixed top-4 right-0 z-50">
          <img
            src="/logo.png"
            alt="Logo"
            className="w-[8rem] max-w-full h-auto object-contain"
          />
        </div>
      </div>

      {/* Content Card */}
      <div className="bg-white rounded-t-3xl rounded-b-2xl shadow-md w-full max-w-xl h-[70vh] flex flex-col overflow-hidden">
        <div className="overflow-y-auto px-6 py-6 flex-1 flex flex-col items-center justify-center space-y-8 text-center" dir="rtl">
          {/* Success Icon */}
          <CheckCircle className="h-16 w-16 text-[#10B981]" />

          {/* Message */}
          <p className="text-lg leading-relaxed text-[#374151] font-[Cairo] font-medium text-center">
            تم استلام مستنداتك بنجاح، وهي قيد المراجعة من قبل الإدارة.
            <br />
            ستتلقى إشعاراً عبر البريد الإلكتروني أو سيتم التواصل معك عبر الهاتف قريباً.
          </p>
          
          

          {/* Back to Home Button */}
          <Button
            onClick={handleBackToHome}
            className="w-full h-12 rounded-full text-white font-medium"
            style={{ backgroundColor: "#E5B62B" }}
          >
            العودة إلى الرئيسية
          </Button>
        </div>
      </div>
    </div>
  )
}
