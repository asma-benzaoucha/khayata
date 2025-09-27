// // pages/AffiliateDashboard.jsx
// import React, { useState } from "react";
// import { Tag, BarChart3, User } from "lucide-react";
// import SidePanel from "../../components/ui/SidePanelAffilie";

// const investmentData = [
//   {
//     id: 1,
//     status: "نشط",
//     statusColor: "text-green-500",
//     endDate: "12/07/2025",
//     activationDate: "12/07/2024",
//     profitPercentage: "10%",
//     discountPercentage: "5%",
//     model: "حجاب صيفي HJB-BEIGE-) عبايةXL K04 (ABK04-NR)",
//     code: "KADI10",
//   },
//   {
//     id: 2,
//     status: "متوقع",
//     statusColor: "text-red-500",
//     endDate: "10/01/2025",
//     activationDate: "12/12/2024",
//     profitPercentage: "5%",
//     discountPercentage: "3%",
//     model: "فيروموني جرير (123123) خيموني صيفي (ABK0404)",
//     code: "KADI2025",
//   },
//   {
//     id: 3,
//     status: "متوقع",
//     statusColor: "text-red-500",
//     endDate: "10/10/2023",
//     activationDate: "12/02/2023",
//     profitPercentage: "5%",
//     discountPercentage: "3%",
//     model: "جلابة فاخرة (DH-HJX-01)",
//     code: "ETE2023",
//   },
//   {
//     id: 3,
//     status: "متوقع",
//     statusColor: "text-red-500",
//     endDate: "10/10/2023",
//     activationDate: "12/02/2023",
//     profitPercentage: "5%",
//     discountPercentage: "3%",
//     model: "جلابة فاخرة (DH-HJX-01)",
//     code: "ETE2023",
//   },
// ];

// export default function AffiliateDashboard() {
//   const menuItems = [
//     { label: "أكواد التخفيض", icon: <Tag size={20} />, path: "/affiliateDashboard/codepromo" },
//     { label: "الإحصائيات", icon: <BarChart3 size={20} />, path: "/affiliateDashboard/statistics" },
//     { label: "حسابي", icon: <User size={20} />, path: "/affiliateDashboard/myAccount" },
//   ];

//   return (
//     <SidePanel menuItems={menuItems}>
//             <div className="flex flex-col w-full h-full space-y-4 pb-4 overflow-x-hidden">

//       {/* Table Header */}
//       <div className="sticky top-0 border-b-[1.5px] border-[#E5B62B] z-10 grid grid-cols-8 gap-4 p-6 bg-gray-50  text-center font-semibold text-[#E5B62B]">
//   <div>#</div>
//   <div>كود التخفيض</div>
//   <div>النماذج المرتبطة</div>
//   <div>نسبة التخفيض للزبون</div>
//   <div>نسبة الربح للأقلية</div>
//   <div>تاريخ التفعيل</div>
//   <div>تاريخ الانتهاء</div>
//   <div>الحالة</div>
// </div>


//       {/* Table Body */}
//       <div className="divide-y divide-gray-200">
//         {investmentData.map((item) => (
//           <div key={item.id} className="grid grid-cols-8 gap-4 p-6 hover:bg-gray-50 transition-colors">
//             <div className="text-center font-semibold text-gray-800">{item.id}</div>
//             <div className="text-center font-semibold text-gray-800">{item.code}</div>
//             <div className="text-center text-gray-700">{item.model}</div>
//             <div className="text-center font-semibold text-gray-800">{item.discountPercentage}</div>
//             <div className="text-center font-semibold text-gray-800">{item.profitPercentage}</div>
//             <div className="text-center text-gray-700">{item.activationDate}</div>
//             <div className="text-center text-gray-700">{item.endDate}</div>
//             <div className="text-center">
//               <span className={`font-semibold ${item.statusColor}`}>{item.status}</span>
//             </div>
//           </div>
//         ))}
//       </div>
//       </div>
//       </SidePanel>
//   );
// }
// pages/AffiliateDashboard.jsx
import React, { useState, useEffect } from "react";
import axiosInstance from "@/utils/axiosInstance"; // ✅ use our configured axios
import { Tag, BarChart3, User } from "lucide-react";
import SidePanel from "../../components/ui/SidePanelAffilie";

export default function AffiliateDashboard() {
  const [promoCodes, setPromoCodes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState({}); // 🔹 track expanded cards in mobile

  const menuItems = [
    { label: "أكواد التخفيض", icon: <Tag size={20} />, path: "/affiliateDashboard/codepromo" },
    { label: "الإحصائيات", icon: <BarChart3 size={20} />, path: "/affiliateDashboard/statistics" },
    { label: "حسابي", icon: <User size={20} />, path: "/affiliate/MyAccount" },
  ];

  useEffect(() => {
    const fetchPromoCodes = async () => {
      try {
        const res = await axiosInstance.get("/affiliate/promocodes/");
        setPromoCodes(res.data);
      } catch (err) {
        console.error("Error fetching promo codes:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchPromoCodes();
  }, []);

  if (loading) {
    return <div className="p-6">جارٍ التحميل...</div>;
  }

  const toggleExpand = (id) => {
    setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <SidePanel menuItems={menuItems}>
      <div className="flex flex-col w-full h-full space-y-4 pb-4 overflow-x-hidden">
        
        {/* ✅ Desktop Table */}
        <div className="hidden md:block">
          <div className="sticky top-0 border-b-[1.5px] border-[#E5B62B] z-10 grid grid-cols-8 gap-4 p-6 bg-gray-50 text-center font-semibold text-[#E5B62B]">
            <div>#</div>
            <div>كود التخفيض</div>
            <div>النماذج المرتبطة</div>
            <div>نسبة التخفيض للزبون</div>
            <div>نسبة الربح للأقلية</div>
            <div>تاريخ التفعيل</div>
            <div>تاريخ الانتهاء</div>
            <div>الحالة</div>
          </div>

          <div className="divide-y divide-gray-200">
            {promoCodes.map((item, index) => (
              <div key={item.id} className="grid grid-cols-8 gap-4 p-6 hover:bg-gray-50 transition-colors">
                <div className="text-center font-semibold text-gray-800">{index + 1}</div>
                <div className="text-center font-semibold text-gray-800">{item.code}</div>
                <div className="text-center text-gray-700">
                  {item.models_CodePromo.map((model) => model.name).join(" , ")}
                </div>
                <div className="text-center font-semibold text-gray-800">{item.discount_percentage}%</div>
                <div className="text-center font-semibold text-gray-800">{item.profit_percentage}%</div>
                <div className="text-center text-gray-700">{item.start_date}</div>
                <div className="text-center text-gray-700">{item.expiration_date}</div>
                <div className="text-center">
                  <span
                    className={`font-semibold ${
                      item.usage_count > 0 ? "text-green-500" : "text-red-500"
                    }`}
                  >
                    {item.usage_count > 0 ? "نشط" : "منتهي"}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* ✅ Mobile Cards */}
        <div className="block md:hidden space-y-4 px-2">
          {promoCodes.map((item) => (
            <div
              key={item.id}
              className="border-2 border-[#999EA6] rounded-2xl p-4 shadow-sm bg-white"
            >
              <div className="flex justify-between items-center">
                <h2 className="font-bold text-gray-800">كود التخفيض: {item.code}</h2>
                <span
                  className={`px-3 py-1 rounded-full text-white text-sm font-semibold ${
                    item.usage_count > 0 ? "bg-green-500" : "bg-red-500"
                  }`}
                >
                  {item.usage_count > 0 ? "نشط" : "منتهي"}
                </span>
              </div>

              <p className="text-sm text-gray-600 mt-2">
                تاريخ التفعيل: {item.start_date}
              </p>
              <p className="text-sm text-gray-600">
                تاريخ الانتهاء: {item.expiration_date}
              </p>

              {/* Toggle Details */}
              {expanded[item.id] && (
                <div className="mt-3 space-y-1 text-sm text-gray-700">
                  <p>نسبة التخفيض للزبون: {item.discount_percentage}%</p>
                  <p>نسبة الربح للأقلية: {item.profit_percentage}%</p>
                  <p>النماذج المرتبطة:</p>
                  <ul className="list-disc list-inside text-gray-700">
                    {item.models_CodePromo.map((model, idx) => (
                      <li key={idx}>{model.name}</li>
                    ))}
                  </ul>
                </div>
              )}

              <button
                onClick={() => toggleExpand(item.id)}
                className="text-blue-600 text-sm mt-2 font-semibold"
              >
                {expanded[item.id] ? "عرض أقل ..." : "عرض المزيد ..."}
              </button>
            </div>
          ))}
        </div>
      </div>
    </SidePanel>
  );
}
