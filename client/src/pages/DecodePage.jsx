import { useNavigate, useOutletContext } from 'react-router-dom';
import { useState } from 'react';
import axios from '../api/axios';

/**
 * Renders decoding page and provides functionality
 * @returns Render of decoding page
 */
export default function DecodePage() {


    const navigate = useNavigate();
    const [encryptionKey, setEncryptionKey] = useState('');
    const [dataOutput, setDataOutput] = useState('');
    const [file, setFile] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);
    const [loading, setLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState(' ');


    // Navigates to splashpage on Return button click
    const handleReturnClick = () => {
        navigate("/")
    };

    // Handle file input change
    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        
        if (selectedFile) {
            // Validate file type (.png or .jpg)
            const fileType = selectedFile.type;
            if (fileType === "image/png" || fileType === "image/jpeg") {
                setFile(selectedFile);
                setErrorMessage('');
                
                // Set image preview
                const objectUrl = URL.createObjectURL(selectedFile);
                setImagePreview(objectUrl);
            } else {
                setFile(null);
                setImagePreview(null);
            }
        }
    };

    // Attempts to decode the image on submit
    const handleFormSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setErrorMessage('');
        setDataOutput(''); // clear previous output
    
        const formData = new FormData();
        formData.append("file", file);
        formData.append("key", encryptionKey);
    
        try {
            const response = await axios.post('/decode/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
    
            const { successful, message } = response.data;
    
            if (successful) {
                setDataOutput(message);
                setErrorMessage('');
            } else {
                setErrorMessage(message);
            }
    
        } catch (error) {
            console.error("Error decoding:", error);
            setErrorMessage('An error occurred while decoding the image.');
        } finally {
            setLoading(false);
        }
    };
    

    // Render components of the decidubg oage
    return (
        <>
            {/* Container which holds all components in form */}
            <div className="container encode-page-container bg-light px-4 pt-2">

                {/* Row containing page title */}
                <div className="row pt-3 text-center">
                    <h4>Encode</h4>
                </div>
                
                <br />

                {/* Row containing file input, text input, and output */}
                <div className="row">

                    {/* Section for file input selection */}
                    <div className="col-6">
                        
                        <div className="row file-input-container">
                            <div className="col-12 d-flex flex-column align-items-center justify-content-center" style={{ height: '100%' }}>

                                {/* Image preview box */}
                                <div 
                                    className="image-preview-box mb-3"
                                    style={{
                                        width: '200px',
                                        height: '200px',
                                        border: '2px solid #007bff',
                                        borderRadius: '8px',
                                        overflow: 'hidden',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        backgroundColor: '#f0f0f0',
                                    }}
                                >
                                    {imagePreview ? (
                                        <img 
                                            src={imagePreview} 
                                            alt="Preview" 
                                            style={{ width: '100%', height: '100%', objectFit: 'fit' }} 
                                        />
                                    ) : (
                                        <p className="text-center">No Media Selected</p>
                                    )}
                                </div>

                                {/* File upload component */}
                                <div className="form-group text-center">
                                    <label htmlFor="fileUpload" className="form-label">Upload Media:</label>
                                    <input 
                                        type="file" 
                                        className="form-control" 
                                        id="fileUpload" 
                                        onChange={ handleFileChange } 
                                        accept=".png, .jpg, .jpeg"
                                        style={{
                                            padding: '10px', 
                                            border: '2px dashed #007bff',
                                            cursor: 'pointer'
                                        }}
                                    />
                                </div>

                            </div>
                        </div>

                    </div>


                    {/* Section for encryption key and data input */}
                    <div className="col-6">

                        {/* Encryption key input field */}
                        <h6 className="mx-1">Enter the Encryption Key:</h6>
                        
                        <div class="input-group">
                            <input 
                                type="text" 
                                class="form-control" 
                                onChange={(e) => setEncryptionKey(e.target.value)}
                            />
                        </div>

                        {/* Data input field */}
                        <h6 className="mx-1 mt-4">Fetched Hidden Data:</h6>

                        <div class="input-group">
                            <textarea 
                                className="form-control" 
                                style={{ resize: 'none', overflow: 'auto', height: '40vw' }}
                                readOnly
                                value={dataOutput}
                            />
                        </div>

                    </div>

                </div>
                    

                {/* Row containing Return and Submit buttons along with sizes and file type */}
                <div className="row py-4 justify-content-evenly">

                    {/* Return button */}
                    <div className="col-2 pt-3 d-grid">
                        <button 
                            type="button" 
                            className="btn btn-secondary"
                            style={{ height: '2vw'}}
                            onClick={ handleReturnClick }>
                            Return
                        </button>
                    </div>

                    {/* Submit button */}
                    <div className="col-2 pt-3 d-grid">
                        <button 
                            type="button" 
                            className="btn btn-success"
                            style={{ height: '2vw'}}
                            onClick={ handleFormSubmit }>
                            Submit
                        </button>
                    </div>

                </div>

                {/* Row for error message */}
                <div className="row text-center" style={{ color: 'red' }}>
                    <p>{ errorMessage }</p>
                </div>

            </div>    
        </>
    );
    
};
