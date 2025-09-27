


// // import React, { useEffect, useState } from "react"
// // import { InputField } from "@/components/ui/inputField"
// // import { PasswordField } from "@/components/ui/passwordField"
// // import { Button } from "@/components/ui/button"
// // import { User, Lock, Pencil } from "lucide-react"
// // import SidePanel from "@/components/ui/SidePanel"
// // import profilIcon from "../../assets/model/profile.png"
// // import passwordIcon from "../../assets/model/security.png"
// // import { toast } from "react-toastify"
// // export default function MonCompte() {
// // const [formData, setFormData] = useState({
// // fullName: "فاطمة أحمد",
// // email: "fatima@gmail.com",
// // phone: "0556263502",
// // address: "المنطقة السكنية الخامسة, ولاية البويرة",
// // currentPassword: "",
// // newPassword: "",
// // confirmPassword: "",
// // })

// // const [errors, setErrors] = useState({})
// // const [editableField, setEditableField] = useState(null) // "fullName" | "email" | "phone" | "address" | null
// // const [showPasswords, setShowPasswords] = useState({ current: false, new: false, confirm: false })

// // // Empêche le body de scroller (c’est le <main> de SidePanel qui scrolle)
// // useEffect(() => {
// // document.body.style.overflow = "hidden"
// // return () => { document.body.style.overflow = "auto" }
// // }, [])

// // // --- Validation (mêmes règles que signup) ---
// // const validateFieldSync = (field, value, current) => {
// // let error = null
// // switch (field) {
// //     case "fullName": {
// //     const arabicRegex = /^[\u0600-\u06FF\s]+$/
// //     if (!value.trim()) error = "الاسم الكامل مطلوب"
// //     else if (!arabicRegex.test(value)) error = "الاسم يجب أن يكون باللغة العربية فقط"
// //     else if (value.trim().length < 2) error = "الاسم يجب أن يكون أكثر من حرفين"
// //     break
// //     }
// //     case "email": {
// //     const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
// //     const hasArabic = /[\u0600-\u06FF]/.test(value)
// //     if (!value) error = "البريد الإلكتروني مطلوب"
// //     else if (!emailRegex.test(value)) error = "البريد الإلكتروني غير صحيح"
// //     else if (hasArabic) error = "البريد الإلكتروني يجب أن يكون بالأحرف اللاتينية فقط"
// //     break
// //     }
// //     case "phone": {
// //     const phoneRegex = /^(0(5|6|7)[0-9]{8}|0[2-4][0-9]{8})$/
// //     if (!value) error = "رقم الهاتف مطلوب"
// //     else if (!phoneRegex.test(value.replace(/\s/g, ""))) error = "رقم الهاتف يجب أن يكون 10 أرقام"
// //     break
// //     }
// //     case "address": {
// //     const arabicRegexAddress = /^[\u0600-\u06FF\s]+$/
// //     if (!value.trim()) error = "عنوان الإقامة مطلوب"
// //     else if (!arabicRegexAddress.test(value)) error = "العنوان يجب أن يكون باللغة العربية فقط"
// //     else if (value.trim().length < 10) error = "العنوان يجب أن يكون أكثر تفصيلاً"
// //     break
// //     }
// //     case "newPassword": {
// //     const hasArabicCharsPassword = /[\u0600-\u06FF]/.test(value)
// //     if (!value) error = "كلمة المرور مطلوبة"
// //     else if (hasArabicCharsPassword) error = "كلمة المرور يجب أن تكون بالأحرف اللاتينية فقط"
// //     else if (value.length < 8) error = "كلمة المرور يجب أن تكون 8 أحرف على الأقل"
// //     else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/.test(value))
// //         error = "كلمة المرور يجب أن تحتوي على حروف كبيرة وصغيرة وأرقام ورموز"
// //     else if (value.trim().toLowerCase() === current.email.trim().toLowerCase())
// //         error = "كلمة المرور لا يجب أن تكون نفس البريد الإلكتروني"
// //     break
// //     }
// //     case "confirmPassword": {
// //     if (!value) error = "تأكيد كلمة المرور مطلوب"
// //     else if (value !== current.newPassword) error = "كلمات المرور غير متطابقة"
// //     break
// //     }
// // }


// // return error
// // }

// // const handleInputChange = (field, value) => {
// // setFormData(prev => {
// //     const next = { ...prev, [field]: value }
// //     const nextErrors = { ...errors }

// //     const e = validateFieldSync(field, value, next)
// //     if (e) nextErrors[field] = e
// //     else delete nextErrors[field]

// //     if (field === "newPassword" || field === "confirmPassword") {
// //     const e1 = validateFieldSync("newPassword", next.newPassword, next)
// //     if (e1) nextErrors.newPassword = e1
// //     else delete nextErrors.newPassword
// //     const e2 = validateFieldSync("confirmPassword", next.confirmPassword, next)
// //     if (e2) nextErrors.confirmPassword = e2
// //     else delete nextErrors.confirmPassword
// //     }
// //     setErrors(nextErrors)
// //     return next
// // })
// // }

// // // Bloque les changements si pas en édition (InputField ne passe pas readOnly)
// // const guardedChange = (field) => (val) => {
// // if (editableField === field) handleInputChange(field, val)
// // }

// // const handleSaveProfile = () => {
// // const fields = ["fullName", "email", "phone", "address"]
// // const newErrors = {}
// // fields.forEach(f => {
// //     const err = validateFieldSync(f, formData[f], formData)
// //     if (err) newErrors[f] = err
// // })
// // setErrors(newErrors)
// // if (Object.keys(newErrors).length > 0) return
// // setEditableField(null)
// // // TODO: appel API sauvegarde
// // }

// // const handleUpdatePassword = () => {
// // const newErrors = {}
// // ;["newPassword", "confirmPassword"].forEach(f => {
// //     const err = validateFieldSync(f, formData[f], formData)
// //     if (err) newErrors[f] = err
// // })
// // setErrors(newErrors)
// // if (Object.keys(newErrors).length > 0) return
// // // TODO: appel API maj mot de passe (currentPassword + newPassword)
// // toast.done("✅ تم تحديث كلمة المرور بنجاح")
// // setFormData(s => ({ ...s, currentPassword: "", newPassword: "", confirmPassword: "" }))
// // }

// // // --- Conditions pour activer/désactiver les boutons ---
// // const isProfileInvalid =
// //   Object.keys(errors).length > 0 ||   editableField === null // pas de champ en édition

// // const isPasswordInvalid =
// //   Object.keys(errors).length > 0 ||   !formData.currentPassword ||  !formData.newPassword ||   !formData.confirmPassword

// // return (
// // <SidePanel>
// //     {/* IMPORTANT : aucun overflow ici, on laisse <main> (dans SidePanel) scroller */}
// //     <div className="w-full h-full min-h-full flex flex-col overflow-x-hidden">
// //     {/* Header sticky centré, full-bleed sans sauter au scroll */}
// //     <div className="sticky top-0 z-20 -mx-6 px-6 bg-white">
// //         <div className="h-14 flex items-center justify-center">
// //         <h1 className="text-3xl font-bold text-[#182544]">الملف الشخصي</h1>
// //         </div>
// //     </div>  

// //     {/* Contenu — PAS d'overflow ici */}
// //     <div className="w-full  space-y-10 px-2 pt-6 pb-16">
// //         {/* --- Section profil --- */}
// //         <div className="flex  items-center gap-2 max-w-[38rem] mx-auto">
// //         <img src={profilIcon} className="w-10 h-10 text-[#182544]" />
// //         <h2 className="font-bold text-2xl text-[#182544]">المعلومات الشخصية</h2>
// //         </div>

// //         <div className="space-y-6 max-w-lg mx-auto">
// //         {/* Nom */}
// //         <div className="relative">
// //             <InputField
// //             label="الاسم الكامل:"
// //             value={formData.fullName}
// //             onChange={guardedChange("fullName")}
// //             error={errors.fullName}
// //             type="text"
// //             placeholder=""
// //             />
// //             <button
// //             type="button"
// //             className="absolute left-4 top-12 text-gray-500 hover:text-gray-700"
// //             onClick={() => setEditableField("fullName")}
// //             aria-label="تعديل الاسم"
// //             title="تعديل"
// //             >
// //             <Pencil className="w-4 h-4" />
// //             </button>
// //         </div>

// //         {/* Email */}
// //         <div className="relative">
// //             <InputField
// //             label="البريد الإلكتروني:"
// //             value={formData.email}
// //             onChange={guardedChange("email")}
// //             error={errors.email}
// //             type="email"
// //             placeholder=""
// //             />
// //             <button
// //             type="button"
// //             className="absolute left-4 top-12 text-gray-500 hover:text-gray-700"
// //             onClick={() => setEditableField("email")}
// //             aria-label="تعديل البريد"
// //             title="تعديل"
// //             >
// //             <Pencil className="w-4 h-4" />
// //             </button>
// //         </div>

// //         {/* Téléphone */}
// //         <div className="relative">
// //             <InputField
// //             label="رقم الهاتف:"
// //             value={formData.phone}
// //             onChange={guardedChange("phone")}
// //             error={errors.phone}
// //             type="tel"
// //             placeholder=""
// //             />
// //             <button
// //             type="button"
// //             className="absolute left-4 top-12 text-gray-500 hover:text-gray-700"
// //             onClick={() => setEditableField("phone")}
// //             aria-label="تعديل الهاتف"
// //             title="تعديل"
// //             >
// //             <Pencil className="w-4 h-4" />
// //             </button>
// //         </div>

// //         {/* Adresse */}
// //         <div className="relative">
// //             <InputField
// //             label="عنوان الإقامة:"
// //             value={formData.address}
// //             onChange={guardedChange("address")}
// //             error={errors.address}
// //             placeholder=""
// //             />
// //             <button
// //             type="button"
// //             className="absolute left-4 top-12 text-gray-500 hover:text-gray-700"
// //             onClick={() => setEditableField("address")}
// //             aria-label="تعديل العنوان"
// //             title="تعديل"
// //             >
// //             <Pencil className="w-4 h-4" />
// //             </button>
// //         </div>

// //         <Button
// //   variant="default"
// //   size="lg"
// //   className="w-64 bg-[#E5B62B] text-white font-bold rounded-xl h-12 disabled:opacity-50 disabled:cursor-not-allowed"
// //   onClick={handleSaveProfile}
// //   disabled={isProfileInvalid}   // 🔴 bouton désactivé si conditions non valides
// // >
// //   حفظ التغيرات
// // </Button>

// //         </div>

// //         {/* --- Section mot de passe --- */}
// //         <div className="space-y-6 ">
// //         <div className="flex  gap-2   max-w-[38rem] mx-auto">
// //             <img src={passwordIcon} className="w-10 h-10" />
// //             <h2 className="font-bold text-2xl text-[#182544]">تغيير كلمة المرور</h2>
// //         </div>
// // <div className="max-w-lg space-y-6 mx-auto">
// //         <PasswordField
// //             label="كلمة المرور الحالية"
// //             placeholder="أدخل كلمة المرور الحالية"
// //             value={formData.currentPassword}
// //             onChange={(v) => handleInputChange("currentPassword", v)}
// //             show={showPasswords.current}
// //             toggleShow={() => setShowPasswords(p => ({ ...p, current: !p.current }))}
// //         />

// //         <PasswordField
// //             label="كلمة المرور الجديدة"
// //             placeholder="يمكنك إنشاء كلمة مرور خاصة بك"
// //             value={formData.newPassword}
// //             onChange={(v) => handleInputChange("newPassword", v)}
// //             error={errors.newPassword}
// //             show={showPasswords.new}
// //             toggleShow={() => setShowPasswords(p => ({ ...p, new: !p.new }))}
// //         />

// //         <PasswordField
// //             label="تأكيد كلمة المرور"
// //             placeholder="أعد كتابة كلمة المرور الجديدة"
// //             value={formData.confirmPassword}
// //             onChange={(v) => handleInputChange("confirmPassword", v)}
// //             error={errors.confirmPassword}
// //             show={showPasswords.confirm}
// //             toggleShow={() => setShowPasswords(p => ({ ...p, confirm: !p.confirm }))}
// //         />
// //         <Button
// //         variant="default"
// //         size="lg"
// //         className="w-64 bg-[#E5B62B] text-white font-bold rounded-xl h-12 disabled:opacity-50 disabled:cursor-not-allowed"
// //         onClick={handleUpdatePassword}
// //         disabled={isPasswordInvalid}  // 🔴 désactivé si conditions non valides
// //         >
// //         تحديث كلمة المرور
// //         </Button>

// //         </div>
// //         <a 
// //   href="/policy" 
// //   target="_blank" 
// //   rel="noopener noreferrer"
// //   className="cursor-pointer flex gap-2 text-xl max-w-[38rem] mx-auto text-[#4A66BD] underline"
// // >
// //   مراجعة شروط وسياسة الاستخدام
// // </a>

// //         </div>
// //     </div>
// //     </div>
// // </SidePanel>
// // )
// // }



// import React, { useEffect, useState } from "react"
// import { InputField } from "@/components/ui/inputField"
// import { PasswordField } from "@/components/ui/passwordField"
// import { Button } from "@/components/ui/button"
// import { Pencil } from "lucide-react"
// import SidePanel from "@/components/ui/SidePanel"
// import profilIcon from "../../assets/model/profile.png"
// import passwordIcon from "../../assets/model/security.png"
// import { toast } from "react-toastify";

// export default function MonCompte() {
//   const [formData, setFormData] = useState({
//     fullName: "",
//     email: "",
//     phone: "",
//     address: "",
//     currentPassword: "",
//     newPassword: "",
//     confirmPassword: "",
// })

// const [errors, setErrors] = useState({})
// const [editableField, setEditableField] = useState(null)
// const [showPasswords, setShowPasswords] = useState({ current: false, new: false, confirm: false })
// const [loading, setLoading] = useState(false)

//   // === 1. Fetch user profile ===
//   useEffect(() => {
//     const fetchProfile = async () => {
//       try {
//         const token = localStorage.getItem("accessToken"); // JWT
//         const res = await fetch("http://127.0.0.1:8000/api/profile/couturiere/", {
//           headers: { Authorization: `Bearer ${token}` },
//         })
//         if (!res.ok) throw new Error("Failed to fetch profile")
//         const data = await res.json()
//         setFormData(prev => ({
//           ...prev,
//           fullName: data.full_name || "",
//           email: data.email || "",
//           phone: data.phone_number || "",
//           address: data.address || "",
//         }))
//       } catch (err) {
//         console.error(err)
//       }
//     }
//     fetchProfile()
//   }, [])

//   // === Validation (synchronous) ===
//   const validateFieldSync = (field, value, current) => {
//     let error = null
//     switch (field) {
//       case "fullName":
//         if (!value.trim()) error = "الاسم الكامل مطلوب"
//         break
//       case "email":
//         if (!value) error = "البريد الإلكتروني مطلوب"
//         break
//       case "phone":
//         if (!value) error = "رقم الهاتف مطلوب"
//         break
//       case "address":
//         if (!value.trim()) error = "عنوان الإقامة مطلوب"
//         break
//       case "newPassword":
//         if (!value) error = "كلمة المرور مطلوبة"
//         else if (value.length < 8) error = "كلمة المرور يجب أن تكون 8 أحرف على الأقل"
//         break
//       case "confirmPassword":
//         if (!value) error = "تأكيد كلمة المرور مطلوب"
//         else if (value !== current.newPassword) error = "كلمات المرور غير متطابقة"
//         break
//       default:
//         break
//     }
//     return error
//   }

//   const handleInputChange = (field, value) => {
//     setFormData(prev => {
//       const next = { ...prev, [field]: value }
//       const nextErrors = { ...errors }
//       const e = validateFieldSync(field, value, next)
//       if (e) nextErrors[field] = e
//       else delete nextErrors[field]
//       setErrors(nextErrors)
//       return next
//     })
//   }

//   const guardedChange = (field) => (val) => {
//     if (editableField === field) handleInputChange(field, val)
//   }

//   // === 2. Save profile ===
//   const handleSaveProfile = async () => {
//     const newErrors = {}
//     ;["fullName", "email", "phone", "address"].forEach(f => {
//       const err = validateFieldSync(f, formData[f], formData)
//       if (err) newErrors[f] = err
//     })
//     setErrors(newErrors)
//     if (Object.keys(newErrors).length > 0) return

//     try {
//       setLoading(true)
//         const token = localStorage.getItem("accessToken"); // JWT
//         const res = await fetch("http://127.0.0.1:8000/api/profile/couturiere/", {
//         method: "PUT",
//         headers: {
//           "Content-Type": "application/json",
//           Authorization: `Bearer ${token}`,
//         },
//         body: JSON.stringify({
//             full_name: formData.fullName,
//           phone_number: formData.phone,
//           address: formData.address,
//         }),
//       })
//       if (!res.ok) throw new Error("Erreur lors de la mise à jour du profil")
//       alert("✅ تم حفظ التغييرات بنجاح")
//       setEditableField(null)
//     } catch (err) {
//         console.error(err)
//         toast.error("فشل في تحديث الملف الشخصي")
      
//     } finally {
//       setLoading(false)
//     }
//   }

//   // === 3. Update password ===
//   const handleUpdatePassword = async () => {
//     const newErrors = {}
//     ;["newPassword", "confirmPassword"].forEach(f => {
//       const err = validateFieldSync(f, formData[f], formData)
//       if (err) newErrors[f] = err
//     })
//     setErrors(newErrors)
//     if (Object.keys(newErrors).length > 0) return

//     try {
//       setLoading(true)
//       const token = localStorage.getItem("accessToken")
//       const res = await fetch("http://127.0.0.1:8000/api/changepasswordWithVerification/couturiere", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//           Authorization: `Bearer ${token}`,
//         },
//         body: JSON.stringify({
//           current_password: formData.currentPassword,
//           new_password: formData.newPassword,
//         }),
//       })
//       if (!res.ok) throw new Error("Erreur lors du changement de mot de passe")
//       toast.success("تم تحديث كلمة المرور بنجاح")
//       setFormData(s => ({ ...s, currentPassword: "", newPassword: "", confirmPassword: "" }))
//     } catch (err) {
//       console.error(err)
//       toast.error("فشل في تغيير كلمة المرور")
//     } finally {
//       setLoading(false)
//     }
//   }

//   const isProfileInvalid = Object.keys(errors).length > 0 || editableField === null
//   const isPasswordInvalid = Object.keys(errors).length > 0 || !formData.currentPassword || !formData.newPassword || !formData.confirmPassword

//   return (
//     <SidePanel>
//       <div className="w-full h-full min-h-full flex flex-col overflow-x-hidden">
//         <div className="sticky top-0 z-20 -mx-6 px-6 bg-white">
//           <div className="h-14 flex items-center justify-center">
//             <h1 className="text-3xl font-bold text-[#182544]">الملف الشخصي</h1>
//           </div>
//         </div>

//         <div className="w-full space-y-10 px-2 pt-6 pb-16">
//           {/* --- Section profil --- */}
//           <div className="flex items-center gap-2 max-w-[38rem] mx-auto">
//             <img src={profilIcon} className="w-10 h-10 text-[#182544]" />
//             <h2 className="font-bold text-2xl text-[#182544]">المعلومات الشخصية</h2>
//           </div>

//           <div className="space-y-6 max-w-lg mx-auto">
//             {/* Full Name */}
//             <div className="relative">
//               <InputField
//                 label="الاسم الكامل:"
//                 value={formData.fullName}
//                 onChange={guardedChange("fullName")}
//                 error={errors.fullName}
//               />
//               <button type="button" className="absolute left-4 top-12 text-gray-500 hover:text-gray-700" onClick={() => setEditableField("fullName")}>
//                 <Pencil className="w-4 h-4" />
//               </button>
//             </div>

//             {/* Email */}
//             <div className="relative">
//               <InputField
//                 label="البريد الإلكتروني:"
//                 value={formData.email}
//                 onChange={guardedChange("email")}
//                 error={errors.email}
//               />
 
//             </div>

//             {/* Phone */}
//             <div className="relative">
//               <InputField
//                 label="رقم الهاتف:"
//                 value={formData.phone}
//                 onChange={guardedChange("phone")}
//                 error={errors.phone}
//               />
//               <button type="button" className="absolute left-4 top-12 text-gray-500 hover:text-gray-700" onClick={() => setEditableField("phone")}>
//                 <Pencil className="w-4 h-4" />
//               </button>
//             </div>

//             {/* Address */}
//             <div className="relative">
//               <InputField
//                 label="عنوان الإقامة:"
//                 value={formData.address}
//                 onChange={guardedChange("address")}
//                 error={errors.address}
//               />
//               <button type="button" className="absolute left-4 top-12 text-gray-500 hover:text-gray-700" onClick={() => setEditableField("address")}>
//                 <Pencil className="w-4 h-4" />
//               </button>
//             </div>

//             <Button
//               variant="default"
//               size="lg"
//               className="w-64 bg-[#E5B62B] text-white font-bold rounded-xl h-12 disabled:opacity-50 disabled:cursor-not-allowed"
//               onClick={handleSaveProfile}
//               disabled={isProfileInvalid || loading}
//             >
//               {loading ? "جارٍ الحفظ..." : "حفظ التغيرات"}
//             </Button>
//           </div>

//           {/* --- Section mot de passe --- */}
//           <div className="space-y-6">
//             <div className="flex gap-2 max-w-[38rem] mx-auto">
//               <img src={passwordIcon} className="w-10 h-10" />
//               <h2 className="font-bold text-2xl text-[#182544]">تغيير كلمة المرور</h2>
//             </div>

//             <div className="max-w-lg space-y-6 mx-auto">
//               <PasswordField
//                 label="كلمة المرور الحالية"
//                 value={formData.currentPassword}
//                 onChange={(v) => handleInputChange("currentPassword", v)}
//                 show={showPasswords.current}
//                 toggleShow={() => setShowPasswords(p => ({ ...p, current: !p.current }))}
//               />

//               <PasswordField
//                 label="كلمة المرور الجديدة"
//                 value={formData.newPassword}
//                 onChange={(v) => handleInputChange("newPassword", v)}
//                 error={errors.newPassword}
//                 show={showPasswords.new}
//                 toggleShow={() => setShowPasswords(p => ({ ...p, new: !p.new }))}
//               />

//               <PasswordField
//                 label="تأكيد كلمة المرور"
//                 value={formData.confirmPassword}
//                 onChange={(v) => handleInputChange("confirmPassword", v)}
//                 error={errors.confirmPassword}
//                 show={showPasswords.confirm}
//                 toggleShow={() => setShowPasswords(p => ({ ...p, confirm: !p.confirm }))}
//               />

//               <Button
//                 variant="default"
//                 size="lg"
//                 className="w-64 bg-[#E5B62B] text-white font-bold rounded-xl h-12 disabled:opacity-50 disabled:cursor-not-allowed"
//                 onClick={handleUpdatePassword}
//                 disabled={isPasswordInvalid || loading}
//               >
//                 {loading ? "جارٍ التحديث..." : "تحديث كلمة المرور"}
//               </Button>
//             </div>
//           </div>
//         </div>
//       </div>
//     </SidePanel>
//   )
// }
import React, { useEffect, useState } from "react"
import { InputField } from "@/components/ui/inputField"
import { PasswordField } from "@/components/ui/passwordField"
import { Button } from "@/components/ui/button"
import { Pencil } from "lucide-react"
import SidePanel from "@/components/ui/SidePanel"
import profilIcon from "../../assets/model/profile.png"
import passwordIcon from "../../assets/model/security.png"
import { toast } from "react-toastify"

export default function MonCompte() {
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    phone: "",
    address: "",
    currentPassword: "",
    newPassword: "",
    confirmPassword: "",
  })

  const [errors, setErrors] = useState({})
  const [editableField, setEditableField] = useState(null)
  const [showPasswords, setShowPasswords] = useState({ current: false, new: false, confirm: false })
  const [loading, setLoading] = useState(false)

  // === 1. Fetch user profile ===
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem("accessToken") // JWT
        const res = await fetch("http://127.0.0.1:8000/api/profile/couturiere/", {
          headers: { Authorization: `Bearer ${token}` },
        })
        if (!res.ok) throw new Error("Failed to fetch profile")
        const data = await res.json()
        setFormData(prev => ({
          ...prev,
          fullName: data.full_name || "",
          email: data.email || "",
          phone: data.phone_number || "",
          address: data.address || "",
        }))
      } catch (err) {
        console.error(err)
      }
    }
    fetchProfile()
  }, [])
// Validation synchronisée des champs
const validateFieldSync = (field, value, currentFormData) => {
let error = null

switch (field) {
    case "fullName": {
    const arabicRegex = /^[\u0600-\u06FF\s]+$/
    if (!value.trim()) {
        error = "الاسم الكامل مطلوب"
    } else if (!arabicRegex.test(value)) {
        error = "الاسم يجب أن يكون باللغة العربية فقط"
    } else if (value.trim().length < 2) {
        error = "الاسم يجب أن يكون أكثر من حرفين"
    }
    break
    }

    case "email":
    if (!value) {
        error = "البريد الإلكتروني مطلوب"
    }
    break

    case "phone": {
    const phoneRegex = /^(0(5|6|7)[0-9]{8}|0[2-4][0-9]{8})$/
    if (!value) {
        error = "رقم الهاتف مطلوب"
    } else if (!phoneRegex.test(value.replace(/\s/g, ""))) {
        error = "رقم الهاتف يجب أن يكون 10 أرقام"
    }
    break
    }

    case "address": {
    const arabicRegexAddress = /^[\u0600-\u06FF\s]+$/
    if (!value.trim()) {
        error = "عنوان الإقامة مطلوب"
    } else if (!arabicRegexAddress.test(value)) {
        error = "العنوان يجب أن يكون باللغة العربية فقط"
    } else if (value.trim().length < 10) {
        error = "العنوان يجب أن يكون أكثر تفصيلاً"
    }
    break
    }

    case "newPassword": {
    const hasArabicCharsPassword = /[\u0600-\u06FF]/.test(value)
    if (!value) {
        error = "كلمة المرور مطلوبة"
    } else if (hasArabicCharsPassword) {
        error = "كلمة المرور يجب أن تكون بالأحرف اللاتينية فقط"
    } else if (value.length < 8) {
        error = "كلمة المرور يجب أن تكون 8 أحرف على الأقل"
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/.test(value)) {
        error = "كلمة المرور يجب أن تحتوي على حروف كبيرة وصغيرة وأرقام ورموز"
    } else if (
        currentFormData.email &&
        value.trim().toLowerCase() === currentFormData.email.trim().toLowerCase()
    ) {
        error = "كلمة المرور لا يجب أن تكون نفس البريد الإلكتروني"
    }
    break
    }

    case "confirmPassword":
    if (!value) {
        error = "تأكيد كلمة المرور مطلوب"
    } else if (value !== currentFormData.newPassword) {
        error = "كلمات المرور غير متطابقة"
    }
    break

    default:
    break
}

return error
}


  const handleInputChange = (field, value) => {
    setFormData(prev => {
      const next = { ...prev, [field]: value }
      const nextErrors = { ...errors }
      const e = validateFieldSync(field, value, next)
      if (e) nextErrors[field] = e
      else delete nextErrors[field]
      setErrors(nextErrors)
      return next
    })
  }

  const guardedChange = (field) => (val) => {
    if (editableField === field) handleInputChange(field, val)
  }

  // === 2. Save profile ===
  const handleSaveProfile = async () => {
    const newErrors = {}
    ;["fullName", "email", "phone", "address"].forEach(f => {
      const err = validateFieldSync(f, formData[f], formData)
      if (err) newErrors[f] = err
    })
    setErrors(newErrors)
    if (Object.keys(newErrors).length > 0) return

    try {
      setLoading(true)
      const token = localStorage.getItem("accessToken") // JWT
      const res = await fetch("http://127.0.0.1:8000/api/profile/couturiere/", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          full_name: formData.fullName,
          phone_number: formData.phone,
          address: formData.address,
        }),
      })
      if (!res.ok) throw new Error("Erreur lors de la mise à jour du profil")
      toast.success("✅ تم حفظ التغييرات بنجاح")
      setEditableField(null)
    } catch (err) {
      console.error(err)
      toast.error("فشل في تحديث الملف الشخصي")
    } finally {
      setLoading(false)
    }
  }

  // === 3. Update password ===
  const handleUpdatePassword = async () => {
    const newErrors = {}
    ;["newPassword", "confirmPassword"].forEach(f => {
      const err = validateFieldSync(f, formData[f], formData)
      if (err) newErrors[f] = err
    })
    setErrors(newErrors)
    if (Object.keys(newErrors).length > 0) return

    try {
      setLoading(true)
      const token = localStorage.getItem("accessToken")
      const res = await fetch("http://127.0.0.1:8000/api/changepasswordWithVerification/couturiere", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          current_password: formData.currentPassword,
          new_password: formData.newPassword,
        }),
      })
      if (!res.ok) throw new Error("Erreur lors du changement de mot de passe")
      toast.success("✅ تم تحديث كلمة المرور بنجاح")
      setFormData(s => ({ ...s, currentPassword: "", newPassword: "", confirmPassword: "" }))
    } catch (err) {
      console.error(err)
      toast.error("فشل في تغيير كلمة المرور")
    } finally {
      setLoading(false)
    }
  }

  // === Validation séparée ===
  const profileFields = ["fullName", "email", "phone", "address"]
  const passwordFields = ["currentPassword", "newPassword", "confirmPassword"]

  const profileErrors = Object.keys(errors).filter(f => profileFields.includes(f))
  const passwordErrors = Object.keys(errors).filter(f => passwordFields.includes(f))

  const isProfileInvalid = profileErrors.length > 0 || editableField === null
  const isPasswordInvalid =
    passwordErrors.length > 0 ||
    !formData.currentPassword ||
    !formData.newPassword ||
    !formData.confirmPassword

    return (
      <SidePanel>
        <div className="w-full h-full min-h-full flex flex-col overflow-x-hidden">
          {/* Header sticky */}
          <div className="sticky top-0 z-20 -mx-6 px-4 sm:px-6 bg-white">
            <div className="h-12 sm:h-14 flex items-center justify-center">
              <h1 className="text-xl sm:text-3xl font-bold text-[#182544]">
                الملف الشخصي
              </h1>
            </div>
          </div>
    
          <div className="w-full space-y-8 sm:space-y-10 px-3 sm:px-2 pt-4 sm:pt-6 pb-12 sm:pb-16">
            {/* --- Section profil --- */}
            <div className="flex items-center gap-2 max-w-[38rem] mx-auto">
              <img src={profilIcon} className="w-6 h-6 sm:w-10 sm:h-10 text-[#182544]" />
              <h2 className="font-bold text-lg sm:text-2xl text-[#182544]">
                المعلومات الشخصية
              </h2>
            </div>
    
            <div className="space-y-4 sm:space-y-6 max-w-lg mx-auto">
              {/* Full Name */}
              <div className="relative">
                <InputField
                  label="الاسم الكامل:"
                  value={formData.fullName}
                  onChange={guardedChange("fullName")}
                  error={errors.fullName}
                />
                <button
                  type="button"
                  className="absolute left-3 top-10 sm:left-4 sm:top-12 text-gray-500 hover:text-gray-700"
                  onClick={() => setEditableField("fullName")}
                >
                  <Pencil className="w-3 h-3 sm:w-4 sm:h-4" />
                </button>
              </div>
    
              {/* Email */}
              <div className="relative">
                <InputField
                  label="البريد الإلكتروني:"
                  value={formData.email}
                  onChange={guardedChange("email")}
                  error={errors.email}
                  disabled
                />
              </div>
    
              {/* Phone */}
              <div className="relative">
                <InputField
                  label="رقم الهاتف:"
                  value={formData.phone}
                  onChange={guardedChange("phone")}
                  error={errors.phone}
                />
                <button
                  type="button"
                  className="absolute left-3 top-10 sm:left-4 sm:top-12 text-gray-500 hover:text-gray-700"
                  onClick={() => setEditableField("phone")}
                >
                  <Pencil className="w-3 h-3 sm:w-4 sm:h-4" />
                </button>
              </div>
    
              {/* Address */}
              <div className="relative">
                <InputField
                  label="عنوان الإقامة:"
                  value={formData.address}
                  onChange={guardedChange("address")}
                  error={errors.address}
                />
                <button
                  type="button"
                  className="absolute left-3 top-10 sm:left-4 sm:top-12 text-gray-500 hover:text-gray-700"
                  onClick={() => setEditableField("address")}
                >
                  <Pencil className="w-3 h-3 sm:w-4 sm:h-4" />
                </button>
              </div>
    
              <Button
                className="w-full sm:w-64 bg-[#E5B62B] hover:bg-[#d4a424] shadow-md text-white font-bold rounded-xl h-10 sm:h-12 text-sm sm:text-base transition disabled:opacity-50 disabled:cursor-not-allowed"
                onClick={handleSaveProfile}
                disabled={isProfileInvalid || loading}
              >
                {loading ? "جارٍ الحفظ..." : "حفظ التغيرات"}
              </Button>
            </div>
    
            {/* --- Section mot de passe --- */}
            <div className="space-y-4 sm:space-y-6">
              <div className="flex gap-2 max-w-[38rem] mx-auto">
                <img src={passwordIcon} className="w-6 h-6 sm:w-10 sm:h-10" />
                <h2 className="font-bold text-lg sm:text-2xl text-[#182544]">
                  تغيير كلمة المرور
                </h2>
              </div>
    
              <div className="max-w-lg space-y-4 sm:space-y-6 mx-auto">
                <PasswordField
                  label="كلمة المرور الحالية"
                  value={formData.currentPassword}
                  onChange={(v) => handleInputChange("currentPassword", v)}
                  show={showPasswords.current}
                  toggleShow={() => setShowPasswords(p => ({ ...p, current: !p.current }))}
                />
    
                <PasswordField
                  label="كلمة المرور الجديدة"
                  value={formData.newPassword}
                  onChange={(v) => handleInputChange("newPassword", v)}
                  error={errors.newPassword}
                  show={showPasswords.new}
                  toggleShow={() => setShowPasswords(p => ({ ...p, new: !p.new }))}
                />
    
                <PasswordField
                  label="تأكيد كلمة المرور"
                  value={formData.confirmPassword}
                  onChange={(v) => handleInputChange("confirmPassword", v)}
                  error={errors.confirmPassword}
                  show={showPasswords.confirm}
                  toggleShow={() => setShowPasswords(p => ({ ...p, confirm: !p.confirm }))}
                />
    
                <Button
                  className="w-full sm:w-64 bg-[#E5B62B] hover:bg-[#d4a424] shadow-md text-white font-bold rounded-xl h-10 sm:h-12 text-sm sm:text-base transition disabled:opacity-50 disabled:cursor-not-allowed"
                  onClick={handleUpdatePassword}
                  disabled={isPasswordInvalid || loading}
                >
                  {loading ? "جارٍ التحديث..." : "تحديث كلمة المرور"}
                </Button>
              </div>
    
              <a 
                href="/policy" 
                target="_blank" 
                rel="noopener noreferrer"
                className="cursor-pointer flex gap-2 text-base sm:text-xl max-w-[38rem] mx-auto text-[#4A66BD] underline"
              >
                مراجعة شروط وسياسة الاستخدام
              </a>
            </div>
          </div>
        </div>
      </SidePanel>
    )
    
}
