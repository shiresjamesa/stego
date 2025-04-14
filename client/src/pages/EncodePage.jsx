import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from '../api/axios';

/**
 * Renders encoding page and provides functionality
 * @returns Render of encoding page
 */
export default function EncodePage() {

    const navigate = useNavigate();
    const [encryptionKey, setEncryptionKey] = useState('');
    const [dataInput, setDataInput] = useState('');
    const dataSizeInBytes = dataInput ? new TextEncoder().encode(dataInput).length : 0;
    const [file, setFile] = useState(null);
    const [fileType, setFileType] = useState(null);
    const [fileSize, setFileSize] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);
    const [downloadUrl, setDownloadUrl] = useState(null);
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
                setFileType(selectedFile.type);
                setFileSize(selectedFile.size);
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

    // Attempts to encode the image on submit
    const handleFormSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setDownloadUrl(null);
        setErrorMessage('');
    
        const formData = new FormData();
        formData.append("file", file);
        formData.append("key", encryptionKey);
        formData.append("data", dataInput);
    
        try {
            const response = await axios.post('/encode/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                responseType: 'blob',
            });
    
            const blob = new Blob([response.data], { type: 'image/png' });
            const url = URL.createObjectURL(blob);
    
            setDownloadUrl(url);
        } catch (error) {
            console.error("Error encoding/downloading:", error);
            setErrorMessage('An error occurred while encoding/downloading the image.');
        } finally {
            setLoading(false);
        }
    };
    
    // Render components of the encode form
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
                    <div className="col-4">
                        
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
                    <div className="col-4">

                        {/* Encryption key input field */}
                        <h6 className="mx-1">Enter an Encryption Key:</h6>
                        
                        <div class="input-group">
                            <input 
                                type="text" 
                                class="form-control" 
                                onChange={(e) => setEncryptionKey(e.target.value)}
                            />
                        </div>

                        {/* Data input field */}
                        <h6 className="mx-1 mt-4">Enter Date to Hide:</h6>

                        <div class="input-group">
                            <textarea 
                                type="textarea" 
                                class="form-control" 
                                style={{ resize: 'none', overflow: 'auto', height: '40vw'}}
                                onChange={(e) => setDataInput(e.target.value)}
                            />
                        </div>

                    </div>


                    {/* Section for encoded file download */}
                    <div className="col-4 d-flex justify-content-center align-items-center" style={{ minHeight: '100%' }}>
                        <div className="text-center">
                            <h5 className="mb-3">File Output</h5>

                            {loading && (
                                <>
                                    <div className="spinner-border my-3" role="status">
                                        <span className="visually-hidden">Loading...</span>
                                    </div>
                                    <p>Encoding in progress...</p>
                                </>
                            )}

                            {!loading && downloadUrl && (
                                <a
                                    href={downloadUrl}
                                    download="encoded.png"
                                    className="btn btn-primary"
                                >
                                    Download Encoded Image
                                </a>
                            )}

                            {!loading && !downloadUrl && (
                                <p>No encoded file yet</p>
                            )}
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

                    {/* Section for data sizes */}
                    <div className="col-2">
                        <div className="d-flex justify-content-between">
                            <span><strong>File Type:</strong></span>
                            <span>{fileType || 'N/A'}</span>
                        </div>
                        <div className="d-flex justify-content-between">
                            <span><strong>File Size:</strong></span>
                            <span>{fileSize ? `${(fileSize / 1024).toFixed(2)} KB` : 'N/A'}</span>
                        </div>
                        <div className="d-flex justify-content-between">
                            <span><strong>Data Size:</strong></span>
                            <span>{dataSizeInBytes} Bytes</span>
                        </div>
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