import React, { useState } from 'react';
import InputField from "../generalComponents/Inputfield";
import compte from '../../assets/icons/compte.png';
import styloIcon from '../../assets/icons/styloIcon.png'; 
import "../../style/compteStyle/Changename.css"
export default function ChangeName() {
  const [nom, setNom] = useState("فاطمة أحمد");
  const [errors, setErrors] = useState("");
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [shake, setShake] = useState(false);

  const handleInputChange = (e) => {
    const value = e.target.value;
    setNom(value);

    if (value.trim() === "") {
      setErrors("يرجى إدخال الاسم");
    } else if (!/^[\p{L}\s]+$/u.test(value)) {
      setErrors("الاسم يجب أن يتكون من حروف فقط");
    } else {
      setErrors(""); // Pas d'erreur
    }
  };

  const isFormValid = () => {
    return errors === "" && nom.trim() !== "";
  };

  return (
   <section className="containerchangename">
  <div className="field-wrapper">
    <section className="nameheader">
      <img src={compte} alt="compte" className="compte-icon" />
      <h1>المعلومات الشخصية</h1>
      
    </section>
<div className="input-wrapper">
  <img src={styloIcon} alt="modifier" className="edit-icon" />
    <InputField
      titre="الاسم الكامل:"
      type="text"
      name="name"
      size="oneline"
      value={nom}
      onChange={handleInputChange}
      hasError={isSubmitted && !!errors} 
      textinfield="فاطمة أحمد"
    />
     
</div>
{isSubmitted && errors && (
      <p className="error">{errors}</p>
    )}
   
  </div>

  <div className="button-group">
    <button
      type="submit"
      className={`btn-confirmcompte ${shake ? "shake" : ""}`}
      onClick={(e) => {
        e.preventDefault();
        setIsSubmitted(true);

        if (isFormValid()) {
          alert("✅ النموذج صالح وجاهز للإرسال!");
          
        } else {
          setShake(true);
          setTimeout(() => setShake(false), 500);
        }
      }}
    >
      حفظ التغييرات
    </button>
  </div>
</section>

  );
}
