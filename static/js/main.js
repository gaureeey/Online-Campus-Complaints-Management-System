/**
 * Online Complaint Management System (OCMS)
 * Beginner-Friendly Client Interactions
 * - Copy tracking number to clipboard with visual feedback
 * - Submit button loading state to prevent double submissions
 * - File validation & thumbnail preview
 * - Interactive 5-star rating widget
 * - Fast table search
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Auto-dismiss flash alerts after 4 seconds
  const flashAlerts = document.querySelectorAll('.alert-dismissible');
  flashAlerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getInstance(alert);
      if (bsAlert) {
        bsAlert.close();
      }
    }, 4000);
  });

  // 2. Mobile Sidebar Toggle
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.querySelector('.ocms-sidebar');
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function () {
      sidebar.classList.toggle('show');
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function (e) {
      if (sidebar.classList.contains('show') && !sidebar.contains(e.target) && e.target !== sidebarToggle && !sidebarToggle.contains(e.target)) {
        sidebar.classList.remove('show');
      }
    });
  }

  // 3. One-Click Copy Tracking Number Utility
  const copyBtns = document.querySelectorAll('.btn-copy-token');
  copyBtns.forEach(btn => {
    btn.addEventListener('click', function () {
      const token = this.getAttribute('data-token');
      if (token && navigator.clipboard) {
        navigator.clipboard.writeText(token).then(() => {
          const originalHtml = this.innerHTML;
          this.innerHTML = '<i class="bi bi-check2 text-success me-1"></i> Copied!';
          this.classList.add('border-success');
          setTimeout(() => {
            this.innerHTML = originalHtml;
            this.classList.remove('border-success');
          }, 2000);
        });
      }
    });
  });

  // 4. Form Submit Double-Submission Prevention (Loading state)
  const forms = document.querySelectorAll('form:not(.no-disable)');
  forms.forEach(form => {
    form.addEventListener('submit', function (e) {
      if (!this.checkValidity()) {
        return;
      }
      const submitBtn = this.querySelector('button[type="submit"]');
      if (submitBtn && !submitBtn.disabled) {
        submitBtn.dataset.originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
          <span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
          Saving...
        `;
        // Safety timeout to re-enable after 8 seconds
        setTimeout(() => {
          if (submitBtn.disabled) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = submitBtn.dataset.originalText || 'Submit';
          }
        }, 8000);
      }
    });
  });

  // 5. Simplified File Upload Check & Previews (Max 3, 5MB each)
  const fileInput = document.getElementById('complaintAttachments');
  const filePreviewContainer = document.getElementById('filePreviewContainer');
  const dropzone = document.getElementById('uploadDropzone');

  if (fileInput && filePreviewContainer) {
    const handleFiles = () => {
      filePreviewContainer.innerHTML = '';
      const files = Array.from(fileInput.files);

      if (files.length > 3) {
        alert('You can attach a maximum of 3 files. Extra files will be skipped.');
        files.splice(3);
      }

      files.forEach(file => {
        if (file.size > 5 * 1024 * 1024) {
          alert(`"${file.name}" is larger than 5 MB. Please choose a smaller photo or PDF.`);
          return;
        }

        const preview = document.createElement('div');
        preview.className = 'col-sm-4 mb-2';
        const isImg = file.type.startsWith('image/');
        const iconOrThumb = isImg 
          ? `<img src="${URL.createObjectURL(file)}" class="rounded me-2" style="width: 44px; height: 44px; object-fit: cover;">`
          : `<div class="bg-danger-subtle text-danger p-2 rounded me-2 fs-5"><i class="bi bi-file-earmark-pdf"></i></div>`;

        preview.innerHTML = `
          <div class="card p-2 border d-flex flex-row align-items-center">
            ${iconOrThumb}
            <div class="overflow-hidden">
              <span class="small fw-semibold d-block text-truncate" style="max-width: 140px;">${file.name}</span>
              <span class="text-muted" style="font-size: 0.75rem;">${(file.size / (1024*1024)).toFixed(1)} MB</span>
            </div>
          </div>
        `;
        filePreviewContainer.appendChild(preview);
      });
    };

    fileInput.addEventListener('change', handleFiles);

    if (dropzone) {
      ['dragover', 'dragenter'].forEach(name => {
        dropzone.addEventListener(name, (e) => {
          e.preventDefault();
          dropzone.classList.add('dragover');
        });
      });

      ['dragleave', 'drop'].forEach(name => {
        dropzone.addEventListener(name, (e) => {
          e.preventDefault();
          dropzone.classList.remove('dragover');
        });
      });

      dropzone.addEventListener('drop', (e) => {
        fileInput.files = e.dataTransfer.files;
        handleFiles();
      });
    }
  }

  // 6. Fast Table Search Filter
  const tableSearch = document.getElementById('tableSearchInput');
  const targetTable = document.querySelector('.filterable-table');
  if (tableSearch && targetTable) {
    tableSearch.addEventListener('input', function () {
      const q = this.value.toLowerCase().trim();
      const rows = targetTable.querySelectorAll('tbody tr');
      rows.forEach(r => {
        const text = r.textContent.toLowerCase();
        r.style.display = text.includes(q) ? '' : 'none';
      });
    });
  }

  // 7. Interactive Star Feedback Click Handlers
  const starInputs = document.querySelectorAll('.star-rating input');
  const ratingText = document.getElementById('ratingValueText');
  if (starInputs.length && ratingText) {
    const labels = {
      '5': 'Excellent - Resolved perfectly',
      '4': 'Good - Problem fixed',
      '3': 'Average - Satisfactory',
      '2': 'Poor - Delay or partial fix',
      '1': 'Very Poor - Problem persists'
    };
    starInputs.forEach(input => {
      input.addEventListener('change', function () {
        ratingText.textContent = labels[this.value] || '';
      });
    });
  }

  // 8. Plain CSV Export Utility for Reports
  const exportBtn = document.getElementById('exportCsvBtn');
  if (exportBtn) {
    exportBtn.addEventListener('click', function () {
      const table = document.getElementById('reportsTable');
      if (!table) return;

      let csv = 'Tracking Number,Date,Category,Status,Staff\n';
      const rows = table.querySelectorAll('tbody tr');
      rows.forEach(r => {
        const cols = r.querySelectorAll('td');
        if (cols.length >= 5) {
          const rowData = [
            `"${cols[0].innerText.trim()}"`,
            `"${cols[1].innerText.trim()}"`,
            `"${cols[2].innerText.trim()}"`,
            `"${cols[3].innerText.trim()}"`,
            `"${cols[4].innerText.trim()}"`
          ];
          csv += rowData.join(',') + '\n';
        }
      });

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Complaints_Report_${new Date().toISOString().slice(0,10)}.csv`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    });
  }
});
