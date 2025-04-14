import LogoImage from '../../assets/logo.png';

/**
 * Returns a render of the Logo
 */
export default function Logo () {

    return (
        <>  
            <div className="logo">
                <img src={ LogoImage } alt="logo" width="100%" /> 
            </div>
        </>
    );
}