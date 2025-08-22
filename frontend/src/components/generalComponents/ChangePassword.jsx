import React, { useState } from 'react';
import InputField from "../generalComponents/Inputfield";
import lockIcon from '../../assets/icons/lock.png';
import "../../style/compteStyle/ChangePassword.css";

export default function ChangePassword() {
  const [form, setForm] = useState({
    current: '',
    newPass: '',
    confirm: ''
  });

const [errors, setErrors] = useState({
  current: '',
  newPass: '',
  confirm: ''
});  
const [isSubmitted, setIsSubmitted] = useState(false);
  const [shake, setShake] = useState(false);

 

  const handleInputChange = (name, value) => {
    setForm(prev => ({ ...prev, [name]: value }));
   isFormValid();
  };

  const isFormValid = () => {
  let valid = true;
  let newErrors = {
    current: '',
    newPass: '',
    confirm: ''
  };

  if (!form.current) {
    newErrors.current = 'يرجى إدخال كلمة المرور الحالية';
    valid = false;
  }

  if (!form.newPass) {
    newErrors.newPass = 'يرجى إدخال كلمة المرور الجديدة';
    valid = false;
  }

  if (!form.confirm) {
    newErrors.confirm = 'يرجى تأكيد كلمة المرور الجديدة';
    valid = false;
  }

  if (form.newPass && form.confirm && form.newPass !== form.confirm) {
    newErrors.confirm = 'كلمتا المرور غير متطابقتين';
    valid = false;
  }

  setErrors(newErrors);
  return valid;
};


  return (
    <section className="containerchangepassword">
      <div className="field-wrapper">
        <section className="nameheader">
          <img src={lockIcon} alt="lock" className="compte-icon" />
          <h1>تغيير كلمة المرور</h1>
        </section>

        <InputField
          titre="كلمة المرور الحالية"
          placeholder="يمكنك تعبئة كلمة المرور الحالية"
          type="password"
          size="oneline"
          name="current"
          value={form.current}
          onChange={(e) => handleInputChange('current', e.target.value)}
          hasError={isSubmitted && !!errors}
        />
        {isSubmitted && errors.current && (
                  <p className="error">{errors.current}</p>
                )}

        <InputField
          titre="كلمة المرور الجديدة"
          placeholder="يمكنك إنشاء كلمة مرور خاصة بك"
          type="password"
          size="oneline"
          name="newPass"
          value={form.newPass}
         onChange={(e) => handleInputChange('newPass', e.target.value)}
          hasError={isSubmitted && !!errors}
        />
         {isSubmitted && errors.newPass && (
                  <p className="error">{errors.newPass}</p>
                )}

        <InputField
          titre="تأكيد كلمة المرور:"
          placeholder="أعد تعبئة نفس كلمة المرور الجديدة"
          type="password"
          size="oneline"
          name="confirm"
          value={form.confirm}
          onChange={(e) => handleInputChange('confirm', e.target.value)}
          hasError={isSubmitted && !!errors}
        />
{isSubmitted && errors.confirm && (
                  <p className="error">{errors.confirm}</p>
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
          تحديث كلمة المرور
        </button>
      </div>
    </section>
  );
}
