// // src/pages/couturiere/MesModels.jsx
// import React, { useEffect, useState } from "react";
// import SidePanel from "@/components/ui/SidePanel";
// import axios from "axios"; // toujours là, mais inutilisé pour le test
// import { Search } from "lucide-react";
// import { NavLink ,} from "react-router-dom";
// import ModelCard from "@/components/ui/ModelCardCouturiere"
// import dress from "../../assets/model/algerian_dress.png"
// import otherdress from  "../../assets/model/otherdress.png"
// import ModelCardCustomFassou from "../../components/ui/custumOrderCardCouturiere"
// export default function MesModels() {
//   const [models, setModels] = useState(null); // null = loading, [] = vide
//   const [error, setError] = useState(null);

//   // Remplace par l'ID réel (depuis token, localStorage ou props)
//   const couturiereId = localStorage.getItem("couturiereId") || "1";

//   useEffect(() => {
//     // ⛔ On commente l'appel API pour ne pas dépendre du backend
//     /*
//     const fetchModels = async () => {
//       try {
//         setError(null);
//         const res = await axios.get(`http://localhost:3000/api/allmodels/${couturiereId}`);
//         setModels(Array.isArray(res.data) ? res.data : []);
//       } catch (err) {
//         console.error(err);
//         setError("Erreur lors de la récupération des modèles.");
//         setModels([]);
//       }
//     };
//     fetchModels();
//     */

//     // ✅ Simulation du premier cas : aucun modèle
//     setTimeout(() => {
//       setModels([]); // force un tableau vide pour afficher "aucun modèle"
//     }, 500); // délai pour voir l'état "chargement"
//   }, [couturiereId]);

// //   return (
// //     <SidePanel>
     
// //       {/* Loading */}
// //       {models === null && (
// //         <div className="flex flex-col items-center justify-center h-full">
// //           <div className="text-6xl text-gray-400 mb-6">
// //             <Search />
// //           </div>
// //           <p className="text-center text-gray-600 mb-2">Chargement...</p>
// //         </div>
// //       )}

// //       {/* Erreur */}
// //       {error && (
// //         <div className="text-red-500">{error}</div>
// //       )}

// //       {/* Aucun modèle */}
// //       {models !== null && models.length === 0 && (
// //         <div className="h-full flex flex-col items-center justify-center">
// //           <div className="text-7xl text-black mb-6">
// //             {/* <Search size={200} /> */}
// //                 <img src="/search2.png" alt="search" className="h-auto w-[13rem] max-w-full object-contain "/>
// //           </div>

// //           <p className="text-gray-700 mb-2">لا توجد أعمال بعد. يمكنك إضافة أول نموذج الآن!</p>
// //           <button
// //             className="mt-3 text-blue-600 hover:underline"
// //             onClick={() => { /* navigation plus tard */ }}
// //           >
// //             <NavLink to="/AddNewModel">
// //             إضافة نموذج جديد

// //             </NavLink>
// //           </button>
// //         </div>
// //       )}


// //       {/* Liste de modèles */}
// //       {models !== null && models.length > 0 && (
// //         <div className="space-y-4">
// //           <div className="text-right">
// //             <button className="text-blue-600 hover:underline">إضافة نموذج جديد</button>
// //           </div>
// //           {models.map((m) => (
// //             <div key={m.id} className="rounded-lg border p-4 shadow-sm flex justify-between items-center">
// //               <div className="flex-1">
// //                 <h3 className="font-semibold text-right">{m.title || "Titre du modèle"}</h3>
// //                 <div className="text-sm text-gray-600 mt-2 text-right">
// //                   <span className="ml-3">كود : {m.code || "—"}</span>
// //                   <span className="ml-3">سعر : {m.price || "—"}</span>
// //                 </div>
// //               </div>
// //               <div className="flex items-center gap-3">
// //                 <span className="px-3 py-1 rounded-full bg-green-500 text-white">مقبول</span>
// //                 <button className="text-blue-600 hover:underline">عرض المزيد ...</button>
// //               </div>
// //             </div>
// //           ))}
// //         </div>
// //       )}
// //     </SidePanel>
// //   );
// // }
// return(
// <SidePanel>
// <div className="grid gap-6 p-4">

// <ModelCardCustomFassou
//   name="فستان صيفي أنيق"
//   code="1234"
//   pricePerPiece={8000}
//   totalPieces={37}
//   date="2025-05-15"
//   type="نسائي"
//   fabric="دانتيل"
//   description="فستان صيفي أنيق بتصميم بسيط..."
//   // status="غير مقبول"
//   status="قيد التنفيد"

//   images={[
//     dress,
//     otherdress,
//     dress,
//   ]}
//   sizes={[
//     { size: "XL", color: "بيج", quantity: 20, hex: "#f5f5dc" },
//     { size: "XXL", color: "أسود", quantity: 12, hex: "#000000" },
//     { size: "XXXL", color: "أحمر", quantity: 5, hex: "#ff0000" },
//     { size: "XXXL", color: "أحمر", quantity: 5, hex: "#ff0000" },
//     { size: "XXXL", color: "أحمر", quantity: 5, hex: "#ff0000" }
//   ]}
//     deadline="1 شهر"
//   orderType="طلب فاصو"
// />

// <ModelCardCustomFassou
//   name="فستان صيفي أنيق"
//   code="1234"
//   pricePerPiece={8000}
//   totalPieces={37}
//   date="2025-05-15"
//   type="نسائي"
//   fabric="دانتيل"
//   description="فستان صيفي أنيق بتصميم بسيط..."
//   // status="غير مقبول"
//   status="انتهى"

//   images={[
//     dress,
//     otherdress,
//     dress,
//   ]}
//   sizes={[
//     { size: "XL", color: "بيج", quantity: 20, hex: "#f5f5dc" },
//     { size: "XXL", color: "أسود", quantity: 12, hex: "#000000" },
//     { size: "XXXL", color: "أحمر", quantity: 5, hex: "#ff0000" }
//   ]}
//   deadline="1 شهر"
//   orderType="fassou"
// />
// </div>

// </SidePanel>

// );}

// // import React, { useState } from "react";
// // import ImageGalleryModal from "./ImageGalleryModal";

// // export default function ProductCard() {
// //   const [openModal, setOpenModal] = useState(false);

// //   const productImages = [
// //     "/images/img1.jpg",
// //     "/images/img2.jpg",
// //     "/images/img3.jpg",
// //   ];

// //   return (
// //     <div className="p-4">
// //       {/* Card */}
// //       <div className="bg-white p-4 rounded-xl shadow-md">
// //         <img
// //           src={productImages[0]}
// //           alt="product"
// //           className="rounded-lg cursor-pointer"
// //           onClick={() => setOpenModal(true)}
// //         />
// //         <h3 className="mt-2 font-semibold text-lg">فستان عرسي أنيق</h3>
// //       </div>

// //       {/* Modal */}
// //       <ImageGalleryModal
// //         images={productImages}
// //         title="فستان عرسي أنيق كود 1234"
// //         isOpen={openModal}
// //         onClose={() => setOpenModal(false)}
// //       />
// //     </div>
// //   );
// // }



import React, { useEffect, useState } from "react";
import SidePanel from "@/components/ui/SidePanel";
import axios from "axios";
// import { NavLink } from "react-router-dom";
import ModelCard from "@/components/ui/ModelCardCouturiere";
import { getArabicColorLabel } from "@/utils/colorUtils";

export default function Demandes() {
  const [models, setModels] = useState(null); // null = loading
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchModels = async () => {
      try {
        setError(null);
        const token = localStorage.getItem("accessToken"); // JWT
        const res = await axios.get("http://127.0.0.1:8000/api/mesDemandesPersonalise/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setModels(Array.isArray(res.data) ? res.data : []);
      } catch (err) {
        console.error(err);
        setError("Erreur lors de la récupération des modèles.");
        setModels([]);
      }
    };
    fetchModels();
  }, []);

  return (
    <SidePanel>
      {/* Cas chargement */}
      {models === null && (
        <div className="flex flex-col items-center justify-center h-full">
          <img src="/search2.png" alt="loading" className="w-40 h-auto" />
          <p className="text-gray-600 mt-2">جار التحميل ...</p>
        </div>
      )}

      {/* Cas erreur */}
      {error && <div className="text-red-500">{error}</div>}

      {/* Cas aucun modèle */}
      {models !== null && models.length === 0 && (
        <div className="h-full flex flex-col items-center justify-center">
          <img
            src="/search2.png"
            alt="search"
            className="h-auto w-[13rem] max-w-full object-contain"
          />
          <p className="text-gray-700 mb-2">
          لا توجد طلبات محددة لك في الوقت الحالي          </p>
          <p className="text-gray-700 mb-2">  يمكننا أن نوضح أن الطلبات المحددة يمكن إضافتها تلقائيًا في لوحة التحكم بعد الاتفاق معك عبر الهاتف أو البريد الإلكتروني</p>
        </div>
      )}

      {/* Cas modèles existants */}
      {models !== null && models.length > 0 && (
        
        <div className="grid gap-6 p-4">
                    
          {models.map((m) => (
            // <ModelCard
            //   key={m.id}
            //   name={m.name}
            //   code={m.code}
            //   pricePerPiece={m.price_per_piece_for_client}
            //   totalPieces={m.total_pieces}
            //   date={m.created_date}
            //   type={m.type}
            //   description={m.description}
            //   status={m.status} 
            //   images={m.images} 

            //   sizes={m.variants.map((v) => ({
            //     size: v.size,
            //     color: getArabicColorLabel(v.color),
            //     quantity: v.quantity,
            //     hex: v.hex  || "#cccccc",
            //   }))}
            //   priceLabel="للقطعة"
            // />
<ModelCard
          key={m.id}
          name={m.nameorder}
          code={m.codeorder}
          pricePerPiece={m.initial_price}
          totalPieces={m.total_requested_quantity || 0}
          date={m.created_date}
          type={m.model_type}
          description={m.description}
          status={m.state}

          images={m.custom_images}
          sizes={m.variants.map((v) => ({
            size: v.size,
            color: getArabicColorLabel(v.color),
            quantity: v.quantity,
            hex: v.hex  || "#cccccc",
          }))}
          priceLabel="لكل القطع"
          deadline={m.deadline}

        />

          ))}
        </div>
      )}
    </SidePanel>
  );
}

