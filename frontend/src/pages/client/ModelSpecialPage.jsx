import React, { useState, useRef } from 'react';
import Popup from "../../components/generalComponents/Popup";
import { useNavigate } from 'react-router-dom';
import { FaRegSmile } from "react-icons/fa";
import InputField from '../../components/generalComponents/Inputfield';
import Navbarshop from '../../components/shoppingComp/Navbarshop';
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

const sizes = ["S", "M", "L", "XL", "XXL", "3XL", "4XL"];

function ModelSpecialPage() {
  const navigate = useNavigate();
  const [shake, setShake] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const fileInputRef = useRef(null);

  const [products, setProducts] = useState([{ 
    id: Date.now(),
    size: "",
    nbpieces: ""
  }]);

  const [form, setForm] = useState({
    nommodel: "",
    phone: "",
    wilaya: "",
    address: "",
    maxdate: "",
    pdfimg: [],
    description: "",
  });

  const [errors, setErrors] = useState({
    nommodel: "",
    phone: "",
    wilaya: "",
    address: "",
    size: "",
    nbpieces: "",
    maxdate: "",
    pdfimg: "",
    description: "",
  });

  const handleAddLine = () => {
    setProducts([...products, { 
      id: Date.now(),
      size: "",
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
    validateProductField(id, name);
  };

  const validateProductField = (id, name) => {
    let error = "";
    setErrors(prev => ({
      ...prev,
      [`${name}-${id}`]: error
    }));
  };

  // Fonction pour valider l'extension du fichier
  const validateFileExtension = (files) => {
  if (!files || files.length === 0) return false;
  
  const allowedExtensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'];
  
  for (let i = 0; i < files.length; i++) {
    const fileName = files[i].name.toLowerCase();
    const isValid = allowedExtensions.some(ext => fileName.endsWith(ext));
    if (!isValid) return false;
  }
  
  return true;
};

  const validateField = (name, value) => {
    let error = "";

    if (name === "phone") {
      const regex = /^0[5-7][0-9]{8}$/;
      if (!regex.test(value)) error = "يجب أن يتكون الرقم من 10 أرقام";
    }
    if (name === "description") {
  if (value && value.length > 500) {
    error = "الوصف يجب ألا يتجاوز 500 حرفاً";
  }
}
    
    if (name === "maxdate") {
      if (value) {
        const selectedDate = new Date(value);
        const today = new Date();
        today.setHours(0, 0, 0, 0); // Reset time to compare only dates
        
        if (selectedDate <= today) {
          error = "يجب أن يكون التاريخ في المستقبل";
        }
      }
    }

    if (name === "nommodel") {
      if (value && value.length > 20) {
        error = "اسم الموديل يجب ألا يتجاوز 20 حرفاً";
      }
    }

   if (name === "pdfimg") {
  if (value && !validateFileExtension(value)) {
    error = "يُسمح فقط بملفات PDF أو الصور (JPG, PNG, GIF, BMP, WEBP)";
  }
}

    setErrors(prev => ({ ...prev, [name]: error }));
  };

  const handleInputChange = (name, value) => {
    setForm(prev => ({ ...prev, [name]: value }));
    validateField(name, value);
  };

const handleFileChange = (files) => {
  if (files && files.length > 0) {
    handleInputChange('pdfimg', [...form.pdfimg, ...files]);
  }
};

const handleRemoveFile = (index) => {
  const newFiles = [...form.pdfimg];
  newFiles.splice(index, 1);
  handleInputChange('pdfimg', newFiles);
};

  const isFormValid = () => {
    const requiredFields = {
      nommodel: form.nommodel,
      phone: form.phone,
      wilaya: form.wilaya,
      address: form.address,
      pdfimg: form.pdfimg,
      maxdate: form.maxdate,
      description: form.description,
    };

    const newErrors = {};

    // Validation des champs obligatoires du formulaire principal
    Object.entries(requiredFields).forEach(([key, value]) => {
      if (!value || (typeof value === 'string' && value.trim() === "")) {
        newErrors[key] = "الرجاء ملء هذا الحقل لإتمام العملية بنجاح";
      } else if (key === "phone") {
        const regex = /^0[5-7][0-9]{8}$/;
        if (!regex.test(value)) {
          newErrors[key] = "يجب أن يتكون الرقم من 10 أرقام";
        }
      } else if (key === "maxdate") {
        const selectedDate = new Date(value);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        if (selectedDate <= today) {
          newErrors[key] = "يجب أن يكون التاريخ في المستقبل";
        }
      } else if (key === "nommodel") {
        if (value.length > 20) {
          newErrors[key] = "اسم الموديل يجب ألا يتجاوز 20 حرفاً";
        }
      } else if (key === "pdfimg") {
        if (!validateFileExtension(value)) {
          newErrors[key] = "يُسمح فقط بملفات PDF أو الصور (JPG, PNG, GIF, BMP, WEBP)";
        }
      }
    });

    // Validation des champs dans les produits
    products.forEach((product) => {
      if (!product.size || product.size.trim() === "") {
        newErrors[`size-${product.id}`] = "الرجاء ملء الحقلين معا: المقاس، وعدد القطع لإتمام الطلب.";
      }
      if (!product.nbpieces || product.nbpieces.trim() === "") {
        newErrors[`nbpieces-${product.id}`] = "الرجاء ملء الحقلين معا: المقاس، وعدد القطع لإتمام الطلب.";
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
          <ArrowBackIcon className='retouricon' onClick={() => navigate(-2)} style={{cursor: 'pointer'}} />
          <div className='containerformachat'>

            <section className="form-header">
              <h1>تصميم خاص</h1>
              <p>يمكنك ملء المعلومات الضرورية لطلب تصميم خاص بك</p>
            </section>

            <form className="purchase-form" onSubmit={(e) => e.preventDefault()}>
              <div className="field-wrapper">
                <InputField
                  titre="اسم الموديل:"
                  placeholder='فستان أنيق'
                  type="text"
                  name="nommodel"
                  size="oneline"
                  down={false}
                  value={form.nommodel}
                  onChange={(e) => handleInputChange('nommodel', e.target.value)}
                  hasError={isSubmitted && !!errors.nommodel}
                />
                {isSubmitted && errors.nommodel && (
                  <p className="error">{errors.nommodel}</p>
                )}
              </div>
              <div className="field-wrapper">
                <InputField
                  titre="الوصف:"
                  placeholder="أدخل وصفاً مفصلاً لطلبك"
                  type="text"
                  name="description"
                  size="oneline"
                  down={false}
                  value={form.description}
                  onChange={(e) => handleInputChange('description', e.target.value)}
                  hasError={isSubmitted && !!errors.description}
                />
                {isSubmitted && errors.description && (
                  <p className="error">{errors.description}</p>
                )}
              </div>

              {products.map((product) => (
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
                    titre="عدد القطع:" 
                    type="number"  
                    name="nbpieces"
                    placeholder="1" 
                    size="quarter" 
                    down={false}  
                    value={product.nbpieces} 
                    onChange={(e) => handleProductChange(product.id, 'nbpieces', e.target.value)}
                    hasError={isSubmitted && !!errors[`nbpieces-${product.id}`]}
                  />

                  {product.id === products[products.length - 1].id && (
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
                    {(errors[`size-${product.id}`] || errors[`nbpieces-${product.id}`]) && (
                      <p className="error">
                        {errors[`size-${product.id}`] || errors[`nbpieces-${product.id}`]}
                      </p>
                    )}
                  </div>
                  <div className='espace'></div>
                </div>
              ))}



            <div className="field-wrapper">
 <InputField
  titre="ارفاق صورة أو ملف PDF:"
  type="file"
  name="pdfimg"
  size="oneline"
  onChange={handleFileChange}
  hasError={isSubmitted && !!errors.pdfimg}
  accept="image/*,application/pdf"
  multiple={true}
  uploadedFiles={form.pdfimg}
  onRemoveFile={handleRemoveFile}
  inputRef={fileInputRef} // Passez la référence ici
/>
  {isSubmitted && errors.pdfimg && (
    <p className="error">{errors.pdfimg}</p>
  )}
</div>

              <div className="field-wrapper">
                <InputField
                  titre="التاريخ الأقصى للتسليم:"
                  placeholder="jj/mm/yyyy"
                  type="date"
                  name="maxdate"
                  size="oneline"
                  value={form.maxdate}
                  onChange={(e) => handleInputChange('maxdate', e.target.value)}
                  hasError={isSubmitted && !!errors.maxdate}
                />
                {isSubmitted && errors.maxdate && (
                  <p className="error">{errors.maxdate}</p>
                )}
              </div>

              <div className="field-wrapper">
                <InputField
                  titre="رقم الهاتف:"
                  placeholder="مثال: 0695449925"
                  type="number"
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

              <div className="field-wrapper">
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
              </div>

              <div className="field-wrapper">
                <InputField
                  titre="العنوان:"
                  placeholder='البلدية و اسم الحي أو الشارع'
                  type="text"
                  name="address"
                  size="oneline"
                  down={false}
                  value={form.address}
                  onChange={(e) => handleInputChange('address', e.target.value)}
                  hasError={isSubmitted && !!errors.address}
                />
                {isSubmitted && errors.address && (
                  <p className="error">{errors.address}</p>
                )}
              </div>

              <div className="button-group">
                <button
                  type="submit"
                  className={`btn-confirm ${shake ? "shake" : ""}`}
                  onClick={(e) => {
                    e.preventDefault();
                    setIsSubmitted(true);

                    if (isFormValid()) {
                      alert("Formulaire valide et prêt à être envoyé !");
                      setShowPopup(true);
                    } else {
                      setShake(true); // Active le tremblement
                      setTimeout(() => setShake(false), 500); // Désactive après 0.5s
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
                        setShowPopup(false);
                        navigate('/special');
                      }, 400);
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

export default ModelSpecialPage;