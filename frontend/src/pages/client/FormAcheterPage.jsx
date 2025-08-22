import React, { useState } from 'react';
import Popup from "../../components/generalComponents/Popup";
import { useNavigate } from 'react-router-dom';

import InputField from '../../components/generalComponents/Inputfield';
import Navbarshop from '../../components/shoppingComp/Navbarshop';
import modelImage from '../../assets/products/p1.png';
import plus from '../../assets/icons/plus.png';
import remove from '../../assets/icons/remove.png';
import "../../style/FormAcheterStyle/FormAcheter.css";
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import donepopup from "../../assets/icons/donepopup.png"
const wilayas = [
  "أدرار", "الشلف", "الأغواط", "أم البواقي", "باتنة", "بجاية", "بسكرة", "بشار",
  "البليدة", "البويرة", "تمنراست", "تبسة", "تلمسان", "تيارت", "تيزي وزو", "الجزائر",
  "الجلفة", "جيجل", "سطيف", "سعيدة", "سكيكدة", "سيدي بلعباس", "عنابة", "قالمة",
  "قسنطينة", "المدية", "مستغانم", "المسيلة", "معسكر", "ورقلة", "وهران", "البيض",
  "إليزي", "برج بوعريريج", "بومرداس", "الطارف", "تندوف", "تيسمسيلت",
  "الوادي", "خنشلة", "سوق أهراس", "تيبازة", "ميلة", "عين الدفلى", "النعامة", "عين تموشنت",
  "غرداية", "غليزان", "تيميمون", "برج باجي مختار", "أولاد جلال", "بني عباس",
  "عين صالح", "عين قزّام", "تقرت", "جانت", "المغير", "المنيعة"
];

const colors = ["أبيض", "أسود", "أحمر", "أزرق", "أخضر", "أصفر", "وردي"];
const sizes = ["S", "M", "L", "XL", "XXL", "3XL", "4XL"];


  const prixProduit = 15000;
  const prixLivraison = 500;
  const total = prixProduit + prixLivraison;
function FormAcheterPage() {
  

  const navigate = useNavigate();

  const [showPopup, setShowPopup] = useState(false);

  const [isSubmitted, setIsSubmitted] = useState(false);

  const [products, setProducts] = useState([{ 
    id: Date.now(),
    size: "",
    color: "",
    nbpieces: ""
  }]);

  const [form, setForm] = useState({
    discountCode: "",
    phone: "",
    wilaya: "",
    address: ""
  });

  const [errors, setErrors] = useState({
    phone: "",
    wilaya: "",
    address: "",
    size: "",
    color: "",
    nbpieces: "",

  });

  const handleAddLine = () => {
    setProducts([...products, { 
      id: Date.now(),
      size: "",
      color: "",
      nbpieces: ""
    }]);
  };

  const handleRemoveLine = (id) => {
    if (products.length > 1) {
      setProducts(products.filter(product => product.id !== id));
    }
  };

  const handleProductChange = (id, name, value) => {
    setProducts(products.map(product => 
      product.id === id ? { ...product, [name]: value } : product
    ));
    validateProductField(id, name, value);
  };
  const validateProductField = (id, name, value) => {
  let error = "";
  if (!value || value.trim() === "") {
      error = "الرجاء ملء هذا الحقل لإتمام العملية بنجاح";
  }

  setErrors(prev => ({
    ...prev,
    [`${name}-${id}`]: error
  }));
};

  const validateField = (name, value) => {
    let error = "";

    if (name === "phone") {
      const regex = /^0[5-7][0-9]{8}$/;
      if (!regex.test(value)) error = "الرقم غير صحيح ";
    }
    else if (name !== "discountCode") {
            if (value==="" || value.trim()==="") { 
      error = "الرجاء ملء هذا الحقل لإتمام العملية بنجاح";
    }
    }

    setErrors(prev => ({ ...prev, [name]: error }));
  };

  const handleInputChange = (name, value) => {
    setForm(prev => ({ ...prev, [name]: value }));
    validateField(name, value);
  };

const isFormValid = () => {
  const requiredFields = {
    phone: form.phone,
    wilaya: form.wilaya,
    address: form.address,
  };

  const newErrors = {};

  // Validation des champs obligatoires du formulaire principal
  Object.entries(requiredFields).forEach(([key, value]) => {
    if (!value || value.trim() === "") {
      newErrors[key] = "الرجاء ملء هذا الحقل لإتمام العملية بنجاح";

    } else if (key === "phone") {
      const regex = /^0[5-7][0-9]{8}$/;
      if (!regex.test(value)) {
        newErrors[key] = "الرقم غير صحيح ";
      }
       
    }
   
  });

  // Validation des champs dans les produits
products.forEach((product, index) => {
  if (!product.size || product.size.trim() === "") {
    newErrors[`size-${product.id}`] = "الرجاء ملء جميع الحقول: المقاس، اللون وعدد القطع، معًا لإتمام الطلب.";
  }
  if (!product.color || product.color.trim() === "") {
    newErrors[`color-${product.id}`] = "الرجاء ملء جميع الحقول: المقاس، اللون وعدد القطع، معًا لإتمام الطلب.";
  }
  if (!product.nbpieces || product.nbpieces.trim() === "") {
    newErrors[`nbpieces-${product.id}`] = "الرجاء ملء جميع الحقول: المقاس، اللون وعدد القطع، معًا لإتمام الطلب.";
  }
});


  setErrors(newErrors);
  return Object.keys(newErrors).length === 0;
};


  return (
    <>
      <Navbarshop defaultSection="" />
      <div className="containershop">
        <div className="shop-wrapper">
          <ArrowBackIcon className='retouricon' />
          <div className='containerformachat'>

            <section className="form-header">
              <h2>شراء الموديل</h2>
              <p>يرجى ملء المعلومات أدناه لإتمام عملية الشراء</p>
            </section>

            <section className="product-details">
              <div className="product-info">
                <img src={modelImage} alt="عباءة محتشمة" className="product-image" />
                <div className='detailproductinfo'>
                  <h3>عباءة محتشمة</h3>
                  <p>{prixProduit} دج</p>
                </div>
              </div>
            </section>

            <form className="purchase-form" onSubmit={(e) => e.preventDefault()}>
              {products.map((product, index) => (
                <div className="flex-row" key={product.id} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <InputField 
                    titre="المقاس:" 
                    type="text" 
                    name="size" 
                    placeholder="S" 
                    size="quarter" 
                    down={true} 
                    value={product.size} 
                    onChange={(e) => handleProductChange(product.id, 'size', e.target.value)}
                    hasError={isSubmitted && !!errors[`size-${product.id}`]}
                    options={sizes}

                  />
 


                  <InputField 
                    titre="اللون" 
                    type="text" 
                    name="color" 
                    placeholder="وردي" 
                    size="quarter" 
                    down={true} 
                    value={product.color} 
                    onChange={(e) => handleProductChange(product.id, 'color', e.target.value)}
                    hasError={isSubmitted && !!errors[`color-${product.id}`]}
                    options={colors}

                  />
                 



                  <InputField 
                    titre="عدد القطع:" 
                    type="text"  
                    name="nbpieces"
                    placeholder="1" 
                    size="quarter" 
                    down={false}  
                    value={product.nbpieces} 
                    onChange={(e) => handleProductChange(product.id, 'nbpieces', e.target.value)}
                    hasError={isSubmitted && !!errors[`nbpieces-${product.id}`]}

                  />
               
  


                  {index === products.length - 1 && (
                    <img
                      src={plus}
                      alt="plus"
                      className="iconplus"
                      onClick={handleAddLine}
                      style={{ cursor: "pointer", width: "25px", height: "25px" }}
                    />
                  )}
                  {products.length > 1 && (
                    <img
                      src={remove}
                      alt="minus"
                      className="minus"
                      onClick={() => handleRemoveLine(product.id)}
                      style={{ cursor: 'pointer', width: '25px', height: '25px' }}
                    />
                  )}
                 <div className='errorsauterlaligne'>
  {(errors[`size-${product.id}`] || errors[`color-${product.id}`] || errors[`nbpieces-${product.id}`]) && (
    <p className="error">
      {errors[`size-${product.id}`] || errors[`color-${product.id}`] || errors[`nbpieces-${product.id}`]}
    </p>
  )}
</div>


                </div>
              ))}
<div className="field-wrapper">
              <InputField
                titre="كود الخصم(إختياري):"
                placeholder="إذا حصلت عليه من طرف مروج الموديل"
                type="text"
                name="discountCode"
                size="oneline"
                down={false}
                value={form.discountCode}
                onChange={(e) => handleInputChange('discountCode', e.target.value)}
  hasError={isSubmitted && !!errors.discountCode}

              />
              </div>
<div className="field-wrapper">
              <InputField
                titre="رقم الهاتف:"
                placeholder="مثال: 0695449925"
                type="text"
                name="phone"
                size="oneline"
                down={false}
                value={form.phone}
                onChange={(e) => handleInputChange('phone', e.target.value)}
  hasError={isSubmitted && !!errors.phone}
                
              />
{isSubmitted && errors.phone && (
  <p className="error">{errors.phone}</p>
)}
</div>
              <InputField
  titre="الولاية:"
  name="wilaya"
  down={true}
  placeholder="الجزائر"
  size="oneline"
  value={form.wilaya}
  onChange={(e) => handleInputChange('wilaya', e.target.value)}
  options={wilayas}
  hasError={isSubmitted && !!errors.wilaya}
/>
{isSubmitted && errors.wilaya && (
  <p className="error">{errors.wilaya}</p>
)}

              <InputField
                titre="العنوان:"
                placeholder='البلدية و اسم الحي أو الشارع'
                type="text"
                name="address"
                size="oneline"
                down={false}
                value={form.address}
                onChange={(e) => handleInputChange('address', e.target.value)}
                hasError={isSubmitted && !!errors[`address-${form.id}`]}
              />
{isSubmitted && errors.address && (
  <p className="error">{errors.address}</p>
)}
              <section className="price-summary">
                <div className="price-row">
                  <span>السعر الأساسي:</span>
                  <span>{prixProduit} دج</span>
                </div>
                <div className="price-row">
                  <span>سعر التوصيل:</span>
                  <span>{prixLivraison} دج</span>
                </div>
                <div className="price-row total">
                  <span style={{ color: "#22C55E" }}>المجموع:</span>
                  <span style={{ color: "#22C55E" }}>{total} دج</span>
                </div>
              </section>

              <div className="button-group">
               <button
  type="submit"
  className="btn-confirm"
  onClick={(e) => {
    e.preventDefault();
    setIsSubmitted(true);
    if (isFormValid()) {
      // Soumission ici
      alert("Formulaire valide et prêt à être envoyé !");
      setShowPopup(true);
      
    }
    

  }}
>
  تأكيد الشراء
</button>
 {showPopup && (
         <Popup
          title="تم استلام طلبيتك "
          iconPopup={donepopup}
          contenu="سنتواصل معك قريبا عبر مكالمة هاتفية أو عبر الواتساب لتأكيد عملية التوصيل. "
          buttonTexte="حسنا"
          onClose={() => setShowPopup(false)}
         onConfirm={() => {

  setTimeout(() => {
    setShowPopup(false);  // ferme réellement
    navigate('/shopping'); // puis navigation douce
  }, 400); // attendre la durée de l'animation CSS
}}

        />
      )}
               
              </div>
            </form>
          </div>
        </div>
      </div>
    </>
  );
}

export default FormAcheterPage;