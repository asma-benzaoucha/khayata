
import ChangeNameComp from '../../components/generalComponents/ChangePassword';
import ChangeName from '../../components/compteComp/ChangeName';
import Navbarshop from '../../components/shoppingComp/Navbarshop';
export default function CompteclientPage(){
return(
<>
      <Navbarshop defaultSection="" />
      <div className="containershop">
        <div className="shop-wrapper">
            
                <section className="form-header">
              <h1>الملف الشخصي</h1>
              
            </section>
            
 <ChangeName />
<ChangeNameComp/>
   

        </div>
        </div>
        </>
        );
        }
