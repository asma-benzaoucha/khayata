// src/components/Cards.jsx
import React from "react";
import ProductCard from "./ProductCard";
import "../../style/shoppingStyle/Cards.css";
import { TbBoxOff } from "react-icons/tb";// Icône de boîte vide (tu peux changer)


  export default function Cards({ products }) {
  const hasProducts = products.length > 0;

  return (
    <div
      className={hasProducts ? "cards-container" : "cards-empty-container"}
    >
      {hasProducts ? (
        products.map((prod) => (
          <ProductCard key={prod.id} product={prod} />
        ))
      ) : (
        <div className="empty-message">
          <TbBoxOff size={60} color="#999" />
          <p>لا يوجد أي موديل حالياً</p>
        </div>
      )}
    </div>
  );
}


