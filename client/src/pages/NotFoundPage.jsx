import { useNavigate } from "react-router-dom";

/**
 * Contains render of page not found form
 * @returns Render of 404 page
 */
export default function NotFoundPage() {
    
    // Initialize page navigation
    const navigate = useNavigate();

    // Handles return to home button click
    const handleReturnClick = () => {
        navigate('/')
    };

    // Render components of the 404 page
    return (
        <>
            {/* Container which holds all components in form */}
            <div className="page-not-found-container container bg-light py-4">

                {/* Row containing page not found label */}
                <div className="row text-center">
                    <h5>The page you were looking for does not exist.</h5>
                </div>

                {/* Row containing button to return to homepage */}
                <div className="row pt-2 justify-content-center">
                    <div className="col-5 d-grid">
                        <button 
                            type="button" 
                            className="btn btn-primary"
                            onClick={ handleReturnClick }>
                            Return to Home
                        </button>
                    </div>
                </div>

            </div>
        </>
    );

};