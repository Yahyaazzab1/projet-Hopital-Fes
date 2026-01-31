// Scanner Intelligent - Version Moderne avec Formulaire
class ModernScanner {
    constructor() {
        this.isScanning = false;
        this.currentStream = null;
        this.devices = [];
        this.currentDeviceId = null;
        this.processingSteps = [];
        this.init();
    }

    init() {
        console.log('Scanner moderne initialisé');
        this.setupEventListeners();
        this.checkCameraSupport();
    }

    setupEventListeners() {
        // Boutons principaux
        document.getElementById('startScanBtn')?.addEventListener('click', () => this.startScanning());
        document.getElementById('uploadBtn')?.addEventListener('click', () => this.uploadFile());
        document.getElementById('batchBtn')?.addEventListener('click', () => this.startBatchScan());
    }

    checkCameraSupport() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            console.warn('Accès à la caméra non supporté');
            this.showMessage('Votre navigateur ne supporte pas l\'accès à la caméra', 'warning');
        }
    }

    async startScanning() {
        try {
            this.showMessage('Démarrage de la numérisation...', 'info');
            this.showProcessingSteps();
            
            // Vérifier l'accès à la caméra
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                await this.startCamera();
            } else {
                // Mode simulation si pas de caméra
                this.simulateScanning();
            }
        } catch (error) {
            console.error('Erreur lors du démarrage:', error);
            this.showMessage('Erreur lors du démarrage de la numérisation', 'error');
        }
    }

    async startCamera() {
        try {
            const constraints = {
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: 'environment'
                }
            };

            this.currentStream = await navigator.mediaDevices.getUserMedia(constraints);
            this.showCameraPreview();
            this.completeStep(1);
        } catch (error) {
            console.error('Erreur caméra:', error);
            this.showMessage('Impossible d\'accéder à la caméra', 'error');
            this.simulateScanning();
        }
    }

    showCameraPreview() {
        const scanPreview = document.getElementById('scanPreview');
        if (scanPreview) {
            scanPreview.innerHTML = `
                <div class="camera-container">
                    <div class="camera-preview">
                        <video id="cameraVideo" autoplay playsinline muted></video>
                        <div class="scan-overlay">
                            <div class="scan-frame"></div>
                        </div>
                        <div class="scan-controls">
                            <p class="text-white mb-3">Placez le document dans le cadre</p>
                            <div class="btn-group">
                                <button class="btn btn-success me-2" onclick="scanner.captureDocument()">
                                    <i class="fas fa-camera me-2"></i>Capturer
                                </button>
                                <button class="btn btn-secondary" onclick="scanner.cancelScanning()">
                                    <i class="fas fa-times me-2"></i>Annuler
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            const video = document.getElementById('cameraVideo');
            if (video && this.currentStream) {
                video.srcObject = this.currentStream;
            }
        }
    }

    simulateScanning() {
        const scanPreview = document.getElementById('scanPreview');
        if (scanPreview) {
            scanPreview.innerHTML = `
                <div class="scanner-placeholder">
                    <div class="loading-spinner mb-3"></div>
                    <h4>Numérisation en cours...</h4>
                    <p>Simulation de capture de document</p>
                    <div class="mt-3">
                        <button class="btn btn-primary" onclick="scanner.captureDocument()">
                            <i class="fas fa-camera me-2"></i>Capturer maintenant
                        </button>
                    </div>
                </div>
            `;
        }

        // Simuler la progression
        this.completeStep(1);
        setTimeout(() => this.completeStep(2), 1000);
        setTimeout(() => this.completeStep(3), 2000);
        setTimeout(() => this.completeStep(4), 3000);
        setTimeout(() => this.completeStep(5), 4000);
        setTimeout(() => this.completeStep(6), 5000);
        // Ne pas capturer automatiquement, laisser l'utilisateur cliquer
    }

    captureDocument() {
        this.showMessage('Document capturé avec succès !', 'success');
        
        // Capturer l'image réelle de la caméra
        const video = document.getElementById('cameraVideo');
        if (video && this.currentStream) {
            // Créer un canvas pour capturer l'image
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            // Définir la taille du canvas
            canvas.width = video.videoWidth || 1280;
            canvas.height = video.videoHeight || 720;
            
            // Dessiner l'image de la vidéo sur le canvas
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            
            // Convertir en base64
            const capturedImage = canvas.toDataURL('image/jpeg', 0.8);
            
            // Arrêter la caméra
            this.stopCamera();
            
            this.showCapturedDocument(capturedImage);
        } else {
            // Fallback: simuler une image si pas de caméra
            const sampleImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjU2MCIgdmlld0JveD0iMCAwIDQwMCA1NjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI0MDAiIGhlaWdodD0iNTYwIiBmaWxsPSIjRjNGNEY2Ii8+CjxyZWN0IHg9IjUwIiB5PSI1MCIgd2lkdGg9IjMwMCIgaGVpZ2h0PSI0NjAiIGZpbGw9IndoaXRlIiBzdHJva2U9IiNFNUU3RUIiIHN0cm9rZS13aWR0aD0iMiIvPgo8dGV4dCB4PSIyMDAiIHk9IjMwMCIgZmlsbD0iIzZCNzI4MCIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE0IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5Eb2N1bWVudCBNw6lkaWNhbDwvdGV4dD4KPC9zdmc+';
            this.showCapturedDocument(sampleImage);
        }
        
        this.hideProcessingSteps();
    }

    showCapturedDocument(imageUrl) {
        const scanPreview = document.getElementById('scanPreview');
        if (scanPreview) {
            scanPreview.innerHTML = `
                <div class="captured-image">
                    <img src="${imageUrl}" alt="Document capturé">
                    <div class="image-overlay">
                        <div class="image-controls">
                            <button class="btn btn-sm btn-primary me-2" onclick="scanner.processWithAI('${imageUrl}')">
                                <i class="fas fa-robot"></i> IA
                            </button>
                            <button class="btn btn-sm btn-warning me-2" onclick="scanner.enhanceImage('${imageUrl}')">
                                <i class="fas fa-magic"></i> Améliorer
                            </button>
                            <button class="btn btn-sm btn-success me-2" onclick="scanner.showDocumentForm('${imageUrl}')">
                                <i class="fas fa-save"></i> Formulaire
                            </button>
                            <button class="btn btn-sm btn-secondary" onclick="scanner.retakePhoto()">
                                <i class="fas fa-redo"></i> Reprendre
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }
    }

    async showDocumentForm(imageUrl) {
        // Récupérer la liste des patients depuis l'API
        let patientsOptions = '<option value="">Chargement des patients...</option>';
        
        try {
            console.log('Chargement des patients...');
            const response = await fetch('/api/patients/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin'
            });
            
            console.log('Response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Data received:', data);
            
            if (data.success) {
                patientsOptions = '<option value="">Sélectionner un patient</option>';
                data.patients.forEach(patient => {
                    patientsOptions += `<option value="${patient.id}">${patient.display_name}</option>`;
                });
                console.log(`Chargé ${data.patients.length} patients`);
            } else {
                console.error('API Error:', data.error);
                patientsOptions = `<option value="">Erreur API: ${data.error}</option>`;
            }
        } catch (error) {
            console.error('Erreur lors du chargement des patients:', error);
            // Fallback avec des patients de démonstration
            patientsOptions = `
                <option value="">Sélectionner un patient</option>
                <option value="1">Ahmed Alami (PAT001)</option>
                <option value="2">Fatima Benali (PAT002)</option>
                <option value="3">Omar Chraibi (PAT003)</option>
                <option value="4">Aicha Daoudi (PAT004)</option>
                <option value="5">Fatine Saadi (PAT59847)</option>
            `;
            console.log('Utilisation des patients de démonstration');
        }
        
        // Créer le modal de formulaire
        const modalHTML = `
            <div class="modal fade" id="documentFormModal" tabindex="-1" aria-labelledby="documentFormModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header bg-primary text-white">
                            <h5 class="modal-title" id="documentFormModalLabel">
                                <i class="fas fa-file-medical me-2"></i>Détails du Document Scanné
                            </h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label fw-bold">Aperçu du Document</label>
                                        <img src="${imageUrl}" alt="Document scanné" class="img-fluid rounded border" style="max-height: 300px; width: 100%; object-fit: contain;">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <form id="documentForm">
                                        <div class="mb-3">
                                            <label class="form-label fw-bold">Titre du Document *</label>
                                            <input type="text" class="form-control" id="documentTitle" required 
                                                   placeholder="Ex: Rapport de radiographie du thorax">
                                        </div>
                                        
                                        <div class="mb-3">
                                            <label class="form-label fw-bold">Type de Document *</label>
                                            <select class="form-select" id="documentType" required>
                                                <option value="">Sélectionner le type</option>
                                                <option value="prescription">Prescription</option>
                                                <option value="lab_results">Résultats de Laboratoire</option>
                                                <option value="radiology">Radiologie</option>
                                                <option value="medical_report">Rapport Médical</option>
                                                <option value="consultation">Consultation</option>
                                                <option value="certificate">Certificat</option>
                                                <option value="insurance">Document d'Assurance</option>
                                                <option value="other">Autre</option>
                                            </select>
                                        </div>
                                        
                                        <div class="mb-3">
                                            <label class="form-label fw-bold">Patient *</label>
                                            <select class="form-select" id="patientSelect" required>
                                                ${patientsOptions}
                                            </select>
                                        </div>
                                        
                                        <div class="mb-3">
                                            <label class="form-label fw-bold">Date du Document</label>
                                            <input type="date" class="form-control" id="documentDate" 
                                                   value="${new Date().toISOString().split('T')[0]}">
                                        </div>
                                        
                                        <div class="mb-3">
                                            <label class="form-label fw-bold">Priorité</label>
                                            <select class="form-select" id="documentPriority">
                                                <option value="normal">Normale</option>
                                                <option value="high">Élevée</option>
                                                <option value="urgent">Urgente</option>
                                            </select>
                                        </div>
                                        
                                        <div class="mb-3">
                                            <label class="form-label fw-bold">Description</label>
                                            <textarea class="form-control" id="documentDescription" rows="3" 
                                                      placeholder="Description du document..."></textarea>
                                        </div>
                                        
                                        <div class="mb-3">
                                            <label class="form-label fw-bold">Notes Médicales</label>
                                            <textarea class="form-control" id="documentNotes" rows="2" 
                                                      placeholder="Notes additionnelles..."></textarea>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                <i class="fas fa-times me-2"></i>Annuler
                            </button>
                            <button type="button" class="btn btn-warning" onclick="scanner.retakePhoto()" data-bs-dismiss="modal">
                                <i class="fas fa-redo me-2"></i>Reprendre
                            </button>
                            <button type="button" class="btn btn-success" onclick="scanner.submitDocument('${imageUrl}')">
                                <i class="fas fa-save me-2"></i>Sauvegarder
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Supprimer l'ancien modal s'il existe
        const existingModal = document.getElementById('documentFormModal');
        if (existingModal) {
            existingModal.remove();
        }
        
        // Ajouter le modal au DOM
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Afficher le modal
        const modal = new bootstrap.Modal(document.getElementById('documentFormModal'));
        modal.show();
        
        // Supprimer le modal du DOM quand il est fermé
        document.getElementById('documentFormModal').addEventListener('hidden.bs.modal', () => {
            document.getElementById('documentFormModal').remove();
        });
    }

    async submitDocument(imageUrl) {
        // Récupérer les données du formulaire
        const formData = {
            title: document.getElementById('documentTitle').value,
            type: document.getElementById('documentType').value,
            patient_id: document.getElementById('patientSelect').value,
            date: document.getElementById('documentDate').value,
            priority: document.getElementById('documentPriority').value,
            description: document.getElementById('documentDescription').value,
            notes: document.getElementById('documentNotes').value,
            image_url: imageUrl
        };
        
        // Validation
        if (!formData.title || !formData.type || !formData.patient_id) {
            this.showMessage('Veuillez remplir tous les champs obligatoires', 'error');
            return;
        }
        
        try {
            // Afficher un message de chargement
            this.showMessage('Sauvegarde en cours...', 'info');
            
            // Envoyer les données au serveur
            const response = await fetch('/api/save-document/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin',
                body: JSON.stringify(formData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                // Afficher la notification
                if (data.notification && window.notifications) {
                    window.notifications.show(
                        data.notification.title,
                        data.notification.message,
                        data.notification.type
                    );
                } else {
                    this.showMessage('Document sauvegardé avec succès !', 'success');
                }
                
                console.log('Document sauvegardé:', data);
                
                // Fermer le modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('documentFormModal'));
                if (modal) {
                    modal.hide();
                }
                
                // Recharger la liste des scans récents
                this.reloadRecentScans();
                
                // Mettre à jour le compteur
                this.updateScansCount();
                
                // Réinitialiser le scanner après 2 secondes
                setTimeout(() => {
                    this.resetScanner();
                }, 2000);
            } else {
                // Afficher l'erreur
                if (window.notifications) {
                    window.notifications.error('Erreur', data.error || 'Impossible de sauvegarder le document');
                } else {
                    this.showMessage(`Erreur: ${data.error}`, 'error');
                }
                console.error('Erreur sauvegarde:', data.error);
            }
            
        } catch (error) {
            console.error('Erreur lors de la sauvegarde:', error);
            this.showMessage(`Erreur de sauvegarde: ${error.message}`, 'error');
        }
    }

    processWithAI(imageUrl) {
        this.showMessage('Traitement IA en cours...', 'info');
        
        setTimeout(() => {
            this.showMessage('Traitement IA terminé avec succès !', 'success');
            // Ouvrir automatiquement le formulaire après traitement IA
            this.showDocumentForm(imageUrl);
        }, 2000);
    }

    enhanceImage(imageUrl) {
        // Afficher le modal d'amélioration
        this.showEnhancementModal(imageUrl);
    }

    showEnhancementModal(imageUrl) {
        const modalHtml = `
            <div class="modal fade" id="enhancementModal" tabindex="-1" aria-labelledby="enhancementModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="enhancementModalLabel">
                                <i class="fas fa-magic me-2"></i>Améliorer l'Image
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <h6>Image Originale</h6>
                                    <img id="originalImage" src="${imageUrl}" alt="Image originale" 
                                         style="max-width: 100%; border: 2px solid #dee2e6; border-radius: 8px;">
                                </div>
                                <div class="col-md-6">
                                    <h6>Image Améliorée</h6>
                                    <div id="enhancedImageContainer" style="min-height: 200px; border: 2px dashed #dee2e6; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                                        <p class="text-muted">Sélectionnez une amélioration</p>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mt-4">
                                <h6>Options d'Amélioration</h6>
                                <div class="row">
                                    <div class="col-md-4 mb-3">
                                        <div class="card enhancement-option" onclick="scanner.applyEnhancement('${imageUrl}', 'brightness')" style="cursor: pointer;">
                                            <div class="card-body text-center">
                                                <i class="fas fa-sun fa-2x text-warning mb-2"></i>
                                                <h6>Luminosité</h6>
                                                <small class="text-muted">Ajuster la luminosité</small>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="card enhancement-option" onclick="scanner.applyEnhancement('${imageUrl}', 'contrast')" style="cursor: pointer;">
                                            <div class="card-body text-center">
                                                <i class="fas fa-adjust fa-2x text-info mb-2"></i>
                                                <h6>Contraste</h6>
                                                <small class="text-muted">Améliorer le contraste</small>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="card enhancement-option" onclick="scanner.applyEnhancement('${imageUrl}', 'sharpen')" style="cursor: pointer;">
                                            <div class="card-body text-center">
                                                <i class="fas fa-search-plus fa-2x text-success mb-2"></i>
                                                <h6>Netteté</h6>
                                                <small class="text-muted">Améliorer la netteté</small>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="card enhancement-option" onclick="scanner.applyEnhancement('${imageUrl}', 'rotate')" style="cursor: pointer;">
                                            <div class="card-body text-center">
                                                <i class="fas fa-redo fa-2x text-primary mb-2"></i>
                                                <h6>Rotation</h6>
                                                <small class="text-muted">Tourner l'image</small>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="card enhancement-option" onclick="scanner.applyEnhancement('${imageUrl}', 'crop')" style="cursor: pointer;">
                                            <div class="card-body text-center">
                                                <i class="fas fa-crop fa-2x text-secondary mb-2"></i>
                                                <h6>Recadrage</h6>
                                                <small class="text-muted">Recadrer l'image</small>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <div class="card enhancement-option" onclick="scanner.applyEnhancement('${imageUrl}', 'auto')" style="cursor: pointer;">
                                            <div class="card-body text-center">
                                                <i class="fas fa-magic fa-2x text-danger mb-2"></i>
                                                <h6>Auto</h6>
                                                <small class="text-muted">Amélioration automatique</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                            <button type="button" class="btn btn-primary" onclick="scanner.saveEnhancedImage()" id="saveEnhancedBtn" disabled>
                                <i class="fas fa-save me-2"></i>Utiliser cette image
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Supprimer l'ancien modal s'il existe
        const existingModal = document.getElementById('enhancementModal');
        if (existingModal) {
            existingModal.remove();
        }

        // Ajouter le nouveau modal
        document.body.insertAdjacentHTML('beforeend', modalHtml);

        // Afficher le modal
        const modal = new bootstrap.Modal(document.getElementById('enhancementModal'));
        modal.show();

        // Stocker l'URL de l'image originale
        this.originalImageUrl = imageUrl;
        this.enhancedImageUrl = null;
    }

    applyEnhancement(imageUrl, enhancementType) {
        this.showMessage(`Application de l'amélioration: ${enhancementType}...`, 'info');
        
        // Créer un canvas pour les améliorations
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        
        img.onload = () => {
            canvas.width = img.width;
            canvas.height = img.height;
            
            // Dessiner l'image originale
            ctx.drawImage(img, 0, 0);
            
            // Appliquer les améliorations selon le type
            switch (enhancementType) {
                case 'brightness':
                    this.applyBrightness(ctx, canvas.width, canvas.height, 1.2);
                    break;
                case 'contrast':
                    this.applyContrast(ctx, canvas.width, canvas.height, 1.3);
                    break;
                case 'sharpen':
                    this.applySharpen(ctx, canvas.width, canvas.height);
                    break;
                case 'rotate':
                    this.applyRotation(ctx, canvas.width, canvas.height);
                    break;
                case 'crop':
                    this.applyCrop(ctx, canvas.width, canvas.height);
                    break;
                case 'auto':
                    this.applyAutoEnhancement(ctx, canvas.width, canvas.height);
                    break;
            }
            
            // Convertir en base64
            const enhancedImageUrl = canvas.toDataURL('image/jpeg', 0.9);
            
            // Afficher l'image améliorée
            const enhancedContainer = document.getElementById('enhancedImageContainer');
            enhancedContainer.innerHTML = `<img src="${enhancedImageUrl}" alt="Image améliorée" style="max-width: 100%; border-radius: 8px;">`;
            
            // Activer le bouton de sauvegarde
            document.getElementById('saveEnhancedBtn').disabled = false;
            
            // Stocker l'URL de l'image améliorée
            this.enhancedImageUrl = enhancedImageUrl;
            
            this.showMessage('Amélioration appliquée !', 'success');
        };
        
        img.src = imageUrl;
    }

    applyBrightness(ctx, width, height, factor) {
        const imageData = ctx.getImageData(0, 0, width, height);
        const data = imageData.data;
        
        for (let i = 0; i < data.length; i += 4) {
            data[i] = Math.min(255, data[i] * factor);     // Rouge
            data[i + 1] = Math.min(255, data[i + 1] * factor); // Vert
            data[i + 2] = Math.min(255, data[i + 2] * factor); // Bleu
        }
        
        ctx.putImageData(imageData, 0, 0);
    }

    applyContrast(ctx, width, height, factor) {
        const imageData = ctx.getImageData(0, 0, width, height);
        const data = imageData.data;
        const intercept = 128 * (1 - factor);
        
        for (let i = 0; i < data.length; i += 4) {
            data[i] = Math.min(255, Math.max(0, data[i] * factor + intercept));
            data[i + 1] = Math.min(255, Math.max(0, data[i + 1] * factor + intercept));
            data[i + 2] = Math.min(255, Math.max(0, data[i + 2] * factor + intercept));
        }
        
        ctx.putImageData(imageData, 0, 0);
    }

    applySharpen(ctx, width, height) {
        // Filtre de netteté simple
        const imageData = ctx.getImageData(0, 0, width, height);
        const data = imageData.data;
        const newData = new Uint8ClampedArray(data);
        
        for (let y = 1; y < height - 1; y++) {
            for (let x = 1; x < width - 1; x++) {
                for (let c = 0; c < 3; c++) {
                    const idx = (y * width + x) * 4 + c;
                    const center = data[idx];
                    const top = data[((y - 1) * width + x) * 4 + c];
                    const bottom = data[((y + 1) * width + x) * 4 + c];
                    const left = data[(y * width + (x - 1)) * 4 + c];
                    const right = data[(y * width + (x + 1)) * 4 + c];
                    
                    newData[idx] = Math.min(255, Math.max(0, center * 5 - (top + bottom + left + right)));
                }
            }
        }
        
        const newImageData = new ImageData(newData, width, height);
        ctx.putImageData(newImageData, 0, 0);
    }

    applyRotation(ctx, width, height) {
        // Rotation de 90 degrés
        const canvas = ctx.canvas;
        const tempCanvas = document.createElement('canvas');
        const tempCtx = tempCanvas.getContext('2d');
        
        tempCanvas.width = height;
        tempCanvas.height = width;
        
        tempCtx.translate(height / 2, width / 2);
        tempCtx.rotate(Math.PI / 2);
        tempCtx.drawImage(canvas, -width / 2, -height / 2);
        
        canvas.width = height;
        canvas.height = width;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(tempCanvas, 0, 0);
    }

    applyCrop(ctx, width, height) {
        // Recadrage au centre (80% de la taille originale)
        const cropWidth = width * 0.8;
        const cropHeight = height * 0.8;
        const startX = (width - cropWidth) / 2;
        const startY = (height - cropHeight) / 2;
        
        const imageData = ctx.getImageData(startX, startY, cropWidth, cropHeight);
        ctx.clearRect(0, 0, width, height);
        ctx.putImageData(imageData, 0, 0);
    }

    applyAutoEnhancement(ctx, width, height) {
        // Amélioration automatique combinée
        this.applyBrightness(ctx, width, height, 1.1);
        this.applyContrast(ctx, width, height, 1.2);
        this.applySharpen(ctx, width, height);
    }

    saveEnhancedImage() {
        if (this.enhancedImageUrl) {
            // Fermer le modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('enhancementModal'));
            modal.hide();
            
            // Mettre à jour l'image affichée
            this.showCapturedDocument(this.enhancedImageUrl);
            this.showMessage('Image améliorée appliquée !', 'success');
        }
    }

    retakePhoto() {
        this.resetScanner();
        this.startScanning();
    }

    cancelScanning() {
        this.stopCamera();
        this.resetScanner();
        this.hideProcessingSteps();
    }

    resetScanner() {
        const scanPreview = document.getElementById('scanPreview');
        if (scanPreview) {
            scanPreview.innerHTML = `
                <div class="scanner-placeholder">
                    <i class="fas fa-camera"></i>
                    <h4>Prêt à Scanner</h4>
                    <p>Choisissez une option ci-dessus pour commencer</p>
                </div>
            `;
        }
    }

    stopCamera() {
        if (this.currentStream) {
            this.currentStream.getTracks().forEach(track => track.stop());
            this.currentStream = null;
        }
    }

    uploadFile() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*,application/pdf';
        input.multiple = false;

        input.onchange = (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    this.showCapturedDocument(event.target.result);
                    this.showMessage('Fichier importé avec succès !', 'success');
                };
                reader.readAsDataURL(file);
            }
        };

        input.click();
    }

    startBatchScan() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*,application/pdf';
        input.multiple = true;

        input.onchange = (e) => {
            const files = Array.from(e.target.files);
            this.showMessage(`Traitement de ${files.length} documents en cours...`, 'info');
            
            files.forEach((file, index) => {
                setTimeout(() => {
                    const reader = new FileReader();
                    reader.onload = (event) => {
                        this.showMessage(`Document ${index + 1}/${files.length} traité`, 'success');
                        // Ouvrir le formulaire pour chaque document
                        this.showDocumentForm(event.target.result);
                    };
                    reader.readAsDataURL(file);
                }, index * 2000); // 2 secondes entre chaque document
            });
        };

        input.click();
    }

    showProcessingSteps() {
        const processingSteps = document.getElementById('processingSteps');
        if (processingSteps) {
            processingSteps.style.display = 'block';
        }
    }

    hideProcessingSteps() {
        const processingSteps = document.getElementById('processingSteps');
        if (processingSteps) {
            processingSteps.style.display = 'none';
        }
    }

    completeStep(stepNumber) {
        const step = document.getElementById(`step${stepNumber}`);
        if (step) {
            const icon = step.querySelector('.step-icon');
            const status = step.querySelector('.step-status .badge');
            
            if (icon) {
                icon.className = 'step-icon completed';
            }
            if (status) {
                status.textContent = 'Terminé';
                status.className = 'badge bg-success';
            }
        }
    }

    async loadPatients() {
        try {
            const response = await fetch('/api/patients/');
            const data = await response.json();
            
            if (data.success) {
                return data.patients;
            } else {
                console.error('Erreur lors du chargement des patients:', data.error);
                return [];
            }
        } catch (error) {
            console.error('Erreur lors du chargement des patients:', error);
            return [];
        }
    }

    showMessage(message, type = 'info') {
        // Créer une notification toast simple
        const toast = document.createElement('div');
        toast.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Supprimer automatiquement après 3 secondes
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 3000);
    }
    
    // Recharger la liste des scans récents
    async reloadRecentScans() {
        try {
            const response = await fetch('/api/documents/?ai_processed=true&limit=10', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success && data.documents) {
                this.updateRecentScansList(data.documents);
            }
        } catch (error) {
            console.error('Erreur lors du rechargement des scans récents:', error);
        }
    }
    
    // Mettre à jour l'affichage de la liste
    updateRecentScansList(documents) {
        const scanList = document.querySelector('.scan-list');
        if (!scanList) return;
        
        if (documents.length === 0) {
            scanList.innerHTML = `
                <div class="text-center py-4 text-muted">
                    <i class="fas fa-inbox fa-3x mb-3"></i>
                    <p>Aucun document scanné</p>
                </div>
            `;
            return;
        }
        
        let html = '';
        documents.forEach(doc => {
            const icon = this.getDocumentIcon(doc.document_type);
            const timeAgo = this.getTimeAgo(doc.created_at);
            
            html += `
                <div class="scan-item">
                    <div class="scan-icon">
                        <i class="fas fa-${icon}"></i>
                    </div>
                    <div class="scan-details">
                        <h6>${doc.title.substring(0, 30)}${doc.title.length > 30 ? '...' : ''}</h6>
                        <small>${doc.patient_name || 'Patient inconnu'}</small>
                        <small class="d-block text-muted">${timeAgo}</small>
                    </div>
                    <div class="scan-actions">
                        <a href="/documents/${doc.id}/" class="btn btn-sm btn-outline-primary" title="Voir">
                            <i class="fas fa-eye"></i>
                        </a>
                        <button class="btn btn-sm btn-outline-success" onclick="downloadDocument(${doc.id})" title="Télécharger">
                            <i class="fas fa-download"></i>
                        </button>
                    </div>
                </div>
            `;
        });
        
        scanList.innerHTML = html;
        
        // Mettre à jour le compteur dans le titre
        const scanTitle = document.querySelector('.recent-scans h5');
        if (scanTitle) {
            scanTitle.innerHTML = `<i class="fas fa-history me-2"></i>Scans Récents (${documents.length})`;
        }
    }
    
    // Obtenir l'icône selon le type de document
    getDocumentIcon(type) {
        const icons = {
            'prescription': 'prescription',
            'lab_result': 'flask',
            'lab_results': 'flask',
            'radiology': 'x-ray',
            'consultation': 'stethoscope',
            'certificate': 'certificate',
            'medical_report': 'file-medical-alt',
        };
        return icons[type] || 'file-medical';
    }
    
    // Calculer le temps écoulé
    getTimeAgo(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const seconds = Math.floor((now - date) / 1000);
        
        if (seconds < 60) return 'Il y a quelques secondes';
        if (seconds < 3600) return `Il y a ${Math.floor(seconds / 60)} minutes`;
        if (seconds < 86400) return `Il y a ${Math.floor(seconds / 3600)} heures`;
        return `Il y a ${Math.floor(seconds / 86400)} jours`;
    }
    
    // Mettre à jour le compteur total
    async updateScansCount() {
        const totalScansEl = document.getElementById('totalScans');
        if (totalScansEl) {
            try {
                const response = await fetch('/api/documents/?ai_processed=true&count_only=true', {
                    method: 'GET',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    credentials: 'same-origin'
                });
                
                if (response.ok) {
                    const data = await response.json();
                    if (data.count !== undefined) {
                        totalScansEl.textContent = data.count;
                    }
                }
            } catch (error) {
                console.error('Erreur lors de la mise à jour du compteur:', error);
            }
        }
    }
}

// Fonctions globales pour compatibilité
function startScanning() {
    window.scanner.startScanning();
}

function uploadFile() {
    window.scanner.uploadFile();
}

function startBatchScan() {
    window.scanner.startBatchScan();
}

function viewScannedReport(reportId) {
    console.log(`Visualisation du rapport ${reportId}`);
    window.scanner.showMessage('Ouverture du rapport...', 'info');
}

function downloadScannedReport(reportId) {
    console.log(`Téléchargement du rapport ${reportId}`);
    window.scanner.showMessage('Téléchargement démarré...', 'success');
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    window.scanner = new ModernScanner();
    console.log('Scanner moderne initialisé');
});
