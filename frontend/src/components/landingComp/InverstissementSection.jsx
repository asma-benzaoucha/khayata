import whatsapp from "../../assets/icons/whatsapp.png";
import "../../style/landingStyle/InvestissementSection.css";
export default function InverstissementSection() {
return (
    <>
    {/* Investment Section */}
<div className="investment-section">
  <div className="investment-header">
    <h2 className="investment-title">فرصة استثمارية</h2>
    <div className="soustitre">
    هل ترغب في استثمار أموالك في مشروع مربح في مجال الخياطة؟
</div>
    <p className="investment-description">
نحن نبحث عن مستثمرين يشاركوننا هذه المشاريع. الحد الأدنى للاستثمار هو مبلغ بسيط. للمزيد من التفاصيل 
    </p>
  </div>     
                
              </div>
              <div className="containerbutton">
                   <a
                     href="https://chat.whatsapp.com/GHvAxP5Jb5sFNQHqaoRgsw?mode=ac_t"
                     target="_blank"
                    rel="noopener noreferrer"
                    className="whatsapp-btn whats"
                   >
                      تواصل معنا عبر الواتساب
  <img src={whatsapp} alt="WhatsApp" />
</a>
</div>

</>
);
}