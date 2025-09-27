
// import React, { useState } from "react";

// // خريطة من أسماء الألوان الإنجليزية إلى ترجمتها بالعربية
// const COLOR_TRANSLATIONS = {
//   "aliceblue": "أليس أزرق فاتح",
//   "antiquewhite": "أبيض عتيق",
//   "aqua": "أكوا (سماوي)",
//   "aquamarine": "أكوامارين",
//   "azure": "أزرق سماوي",
//   "beige": "بيج",
//   "bisque": "بسكوي",
//   "black": "أسود",
//   "blanchedalmond": "لوزي باهت",
//   "blue": "أزرق",
//   "blueviolet": "بنفسجي مزرق",
//   "brown": "بني",
//   "burlywood": "خشبي",
//   "cadetblue": "أزرق رمادي",
//   "chartreuse": "أخضر مصفر",
//   "chocolate": "شوكولاتة",
//   "coral": "مرجاني",
//   "cornflowerblue": "أزرق زهرة الذرة",
//   "cornsilk": "حرير الذرة",
//   "crimson": "قرمزي",
//   "cyan": "سماوي",
//   "darkblue": "أزرق داكن",
//   "darkcyan": "سماوي داكن",
//   "darkgoldenrod": "ذهبي غامق",
//   "darkgray": "رمادي داكن",
//   "darkgrey": "رمادي داكن",
//   "darkgreen": "أخضر داكن",
//   "darkkhaki": "كاكي داكن",
//   "darkmagenta": "أرجواني داكن",
//   "darkolivegreen": "أخضر زيتوني داكن",
//   "darkorange": "برتقالي داكن",
//   "darkorchid": "أرجواني داكن",
//   "darkred": "أحمر داكن",
//   "darksalmon": "سلموني داكن",
//   "darkseagreen": "أخضر بحري داكن",
//   "darkslateblue": "أزرق أردوازي داكن",
//   "darkslategray": "رمادي أردوازي داكن",
//   "darkslategrey": "رمادي أردوازي داكن",
//   "darkturquoise": "تركوازي داكن",
//   "darkviolet": "بنفسجي داكن",
//   "deeppink": "زهري غامق",
//   "deepskyblue": "أزرق سماوي غامق",
//   "dimgray": "رمادي خافت",
//   "dimgrey": "رمادي خافت",
//   "dodgerblue": "أزرق فاتح",
//   "firebrick": "أحمر قرميدي",
//   "floralwhite": "أبيض زهري",
//   "forestgreen": "أخضر غابة",
//   "fuchsia": "فوشيا",
//   "gainsboro": "رمادي فاتح",
//   "ghostwhite": "أبيض شبحي",
//   "gold": "ذهبي",
//   "goldenrod": "ذهبي غامق",
//   "gray": "رمادي",
//   "grey": "رمادي",
//   "green": "أخضر",
//   "greenyellow": "أخضر مصفر",
//   "honeydew": "عسلي فاتح",
//   "hotpink": "وردي فاقع",
//   "indianred": "أحمر هندي",
//   "indigo": "نيلي",
//   "ivory": "عاجي",
//   "khaki": "كاكي",
//   "lavender": "لافندر",
//   "lavenderblush": "لافندر باهت",
//   "lawngreen": "أخضر عشبي",
//   "lemonchiffon": "ليموني فاتح",
//   "lightblue": "أزرق فاتح",
//   "lightcoral": "مرجاني فاتح",
//   "lightcyan": "سماوي فاتح",
//   "lightgoldenrodyellow": "ذهبي مصفر فاتح",
//   "lightgray": "رمادي فاتح",
//   "lightgrey": "رمادي فاتح",
//   "lightgreen": "أخضر فاتح",
//   "lightpink": "وردي فاتح",
//   "lightsalmon": "سلموني فاتح",
//   "lightseagreen": "أخضر بحري فاتح",
//   "lightskyblue": "أزرق سماوي فاتح",
//   "lightslategray": "رمادي أردوازي فاتح",
//   "lightslategrey": "رمادي أردوازي فاتح",
//   "lightsteelblue": "أزرق فولاذي فاتح",
//   "lightyellow": "أصفر فاتح",
//   "lime": "ليموني",
//   "limegreen": "أخضر ليموني",
//   "linen": "كتاني",
//   "magenta": "ماجنتا",
//   "maroon": "كستنائي",
//   "mediumaquamarine": "أكوامارين متوسط",
//   "mediumblue": "أزرق متوسط",
//   "mediumorchid": "أرجواني متوسط",
//   "mediumpurple": "بنفسجي متوسط",
//   "mediumseagreen": "أخضر بحري متوسط",
//   "mediumslateblue": "أزرق أردوازي متوسط",
//   "mediumspringgreen": "أخضر ربيعي متوسط",
//   "mediumturquoise": "تركوازي متوسط",
//   "mediumvioletred": "أحمر بنفسجي متوسط",
//   "midnightblue": "أزرق ليلي",
//   "mintcream": "نعناعي فاتح",
//   "mistyrose": "وردي ضبابي",
//   "moccasin": "موكاسين",
//   "navajowhite": "أبيض نافاجو",
//   "navy": "أزرق بحري",
//   "oldlace": "عاجي قديم",
//   "olive": "زيتي",
//   "olivedrab": "زيتي باهت",
//   "orange": "برتقالي",
//   "orangered": "برتقالي محمر",
//   "orchid": "أرجواني فاتح",
//   "palegoldenrod": "ذهبي شاحب",
//   "palegreen": "أخضر شاحب",
//   "paleturquoise": "تركوازي شاحب",
//   "palevioletred": "أحمر بنفسجي شاحب",
//   "papayawhip": "بابايا",
//   "peachpuff": "خوخي",
//   "peru": "برونزي",
//   "pink": "وردي",
//   "plum": "برقوقي",
//   "powderblue": "أزرق مسحوقي",
//   "purple": "بنفسجي",
//   "red": "أحمر",
//   "rosybrown": "بني وردي",
//   "royalblue": "أزرق ملكي",
//   "saddlebrown": "بني سرج",
//   "salmon": "سلموني",
//   "sandybrown": "بني رملي",
//   "seagreen": "أخضر بحري",
//   "seashell": "صدفي",
//   "sienna": "بني محمر",
//   "silver": "فضي",
//   "skyblue": "أزرق سماوي",
//   "slateblue": "أزرق أردوازي",
//   "slategray": "رمادي أردوازي",
//   "slategrey": "رمادي أردوازي",
//   "snow": "أبيض ثلجي",
//   "springgreen": "أخضر ربيعي",
//   "steelblue": "أزرق فولاذي",
//   "tan": "بني فاتح",
//   "teal": "أزرق مخضر",
//   "thistle": "أرجواني فاتح",
//   "tomato": "طماطمي",
//   "turquoise": "تركوازي",
//   "violet": "بنفسجي فاتح",
//   "wheat": "قمحي",
//   "white": "أبيض",
//   "whitesmoke": "أبيض مدخن",
//   "yellow": "أصفر",
//   "yellowgreen": "أصفر مخضر"
// };





// const COLOR_OPTIONS = Object.entries(COLOR_TRANSLATIONS).map(
//   ([value, label]) => ({
//     value,
//     label,
//   })
// );

// export default function ColorAutocomplete({ label, value, onChange, error }) {
//   const [query, setQuery] = useState("");
//   const [showDropdown, setShowDropdown] = useState(false);

//   // البحث في القائمة
//   const filteredOptions = COLOR_OPTIONS.filter((opt) =>
//     opt.label.toLowerCase().includes(query.toLowerCase())
//   );

//   return (
//     <div className="space-y-2 text-right relative">
//       <label className="text-sm text-[#374151] font-[Cairo] font-semibold">
//         {label}
//       </label>

//       <div
//         className={`w-full rounded-full px-4 border-[1px] transition-all duration-200 
//           ${error ? "border-red-500" : "border-[#C1C1C1]"} 
//           focus-within:border-[#374151] focus-within:border-[3px] 
//           focus-within:shadow-lg focus-within:border-opacity-50 bg-white`}
//       >
//         <input
//           type="text"
//           value={query || value}
//           onChange={(e) => {
//             setQuery(e.target.value);
//             setShowDropdown(true);
//           }}
//           onFocus={() => setShowDropdown(true)}
//           placeholder="ابحث عن اللون..."
//           className="w-full h-12 bg-transparent outline-none border-none text-right font-[Cairo] text-[15px] font-semibold text-[#374151] placeholder-[#B0B0B0]"
//         />
//       </div>

//       {/* Dropdown */}
//       {showDropdown && query && (
//         <ul className="absolute z-10 mt-1 w-full max-h-48 overflow-y-auto rounded-lg border border-gray-300 bg-white shadow-md">
//           {filteredOptions.length > 0 ? (
//             filteredOptions.map((opt, idx) => (
//               <li
//                 key={idx}
//                 onClick={() => {
//                   onChange(opt.value);
//                   setQuery(opt.label);
//                   setShowDropdown(false);
//                 }}
//                 className="flex items-center justify-end gap-2 px-4 py-2 cursor-pointer hover:bg-gray-100 text-right font-[Cairo]"
//               >
//                 {/* مربع اللون */}
//                 <span
//                   className="w-5 h-5 rounded-full border border-gray-300"
//                   style={{ backgroundColor: opt.value }}
//                 ></span>
//                 {opt.label}
//               </li>
//             ))
//           ) : (
//             <li className="px-4 py-2 text-red-500 font-[Cairo]">لا يوجد تطابق</li>
//           )}
//         </ul>
//       )}

//       {error && <p className="text-red-500 text-xs">{error}</p>}
//     </div>
//   );
// }

import React, { useState } from "react";
import { COLOR_OPTIONS, getArabicColorLabel } from "@/utils/colorUtils";

export default function ColorAutocomplete({ label, value, onChange, error }) {
  const [query, setQuery] = useState("");
  const [showDropdown, setShowDropdown] = useState(false);

  const filteredOptions = COLOR_OPTIONS.filter((opt) =>
    opt.label.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="space-y-2 text-right relative">
      <label className="text-sm text-[#374151] font-[Cairo] font-semibold">
        {label}
      </label>

      <div
        className={`w-full rounded-full px-4 border-[1px] transition-all duration-200 
          ${error ? "border-red-500" : "border-[#C1C1C1]"} 
          focus-within:border-[#374151] focus-within:border-[3px] 
          focus-within:shadow-lg focus-within:border-opacity-50 bg-white`}
      >
        <input
          type="text"
          value={query || getArabicColorLabel(value)}
          onChange={(e) => {
            setQuery(e.target.value);
            setShowDropdown(true);
          }}
          onFocus={() => setShowDropdown(true)}
          placeholder="ابحث عن اللون..."
          className="w-full h-12 bg-transparent outline-none border-none text-right font-[Cairo] text-[15px] font-semibold text-[#374151] placeholder-[#B0B0B0]"
        />
      </div>

      {showDropdown && query && (
        <ul className="absolute z-10 mt-1 w-full max-h-48 overflow-y-auto rounded-lg border border-gray-300 bg-white shadow-md">
          {filteredOptions.length > 0 ? (
            filteredOptions.map((opt, idx) => (
              <li
                key={idx}
                onClick={() => {
                  onChange(opt.value);
                  setQuery(opt.label);
                  setShowDropdown(false);
                }}
                className="flex items-center justify-end gap-2 px-4 py-2 cursor-pointer hover:bg-gray-100 text-right font-[Cairo]"
              >
                <span
                  className="w-5 h-5 rounded-full border border-gray-300"
                  style={{ backgroundColor: opt.value }}
                ></span>
                {opt.label}
              </li>
            ))
          ) : (
            <li className="px-4 py-2 text-red-500 font-[Cairo]">لا يوجد تطابق</li>
          )}
        </ul>
      )}

      {error && <p className="text-red-500 text-xs">{error}</p>}
    </div>
  );
}
