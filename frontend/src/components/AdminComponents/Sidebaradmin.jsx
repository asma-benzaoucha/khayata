import React, { useState } from "react";
import logo from "../../assets/logojaune.png";
import homeBlanc from "../../assets/icons/homeblanc.png"; // Ajoutez cette icône
import homeBleu from "../../assets/icons/home.png";   // Ajoutez cette icône
import commandBlanc from "../../assets/commandeblanc.png"; // Ajoutez cette icône
import commandBleu from "../../assets/icons/commande.png";   // Ajoutez cette icône
import membersblanc from "../../assets/members.png";
import membersbleu from "../../assets/membersbleu.png";
import modelblanc from "../../assets/modelblanc.png";
import modelbleu from "../../assets/modelbleu.png";
import affiliatebleu from "../../assets/affiliatebleu.png";
import affiliateblanc from "../../assets/affiliateblanc.png";
import dropshipperbleu from "../../assets/dropshipperbleu.png";
import dropshipperblanc from "../../assets/dropshipperblanc.png";
import parametreblanc from "../../assets/parametre.png";
import parametrebleu from "../../assets/parametrebleu.png";
import "../../style/AdminStyle/Sidebaradmin.css";
import logout from "../../assets/logout.png"
export default function Sidebaradmin() {
  const [active, setActive] = useState("home");

  const menuItems = [
    { 
      id: "home", 
      label: "لوحة التحكم", 
      icon: active === "home" ? homeBleu : homeBlanc 
    },
    { 
      id: "orders", 
      label: "إدارة الطلبات", 
      icon: active === "orders" ? commandBleu : commandBlanc 
    },
    { 
      id: "members", 
      label: "إدارة العملاء", 
      icon: active === "members" ? membersbleu : membersblanc 
    },
    { 
      id: "models", 
      label: "إدارة النماذج", 
      icon: active === "models" ? modelbleu : modelblanc 
    },
    { 
      id: "affiliates", 
      label: "إدارة المروجين", 
      icon: active === "affiliates" ? affiliatebleu : affiliateblanc 
    },
    { 
      id: "dropshipping", 
      label: "إدارة الدروبشيبينغ", 
      icon: active === "dropshipping" ? dropshipperbleu : dropshipperblanc 
    },
    { 
      id: "settings", 
      label: "الإعدادات", 
      icon: active === "settings" ? parametrebleu : parametreblanc 
    },
  ];

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <img src={logo} alt="logo" className="sidebar-logo" />
      </div>
      <ul className="sidebar-menu">
        {menuItems.map((item) => (
          <li
            key={item.id}
            className={`sidebar-item ${active === item.id ? "active" : ""}`}
            onClick={() => setActive(item.id)}
          >
            <img src={item.icon} alt={item.label} className="sidebar-icon" />
            <span className={`sidebar-text ${active === item.id ? "active" : ""}`}>
              {item.label}
            </span>
          </li>
        ))}
      </ul>
      <div className="sidebar-footer">
        <button className="logout-btn">
          <img src={logout} alt="تسجيل الخروج" className="logout-icon" />
          تسجيل الخروج
        </button>
      </div>
    </div>
  );
}