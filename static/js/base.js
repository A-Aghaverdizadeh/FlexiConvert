var url = window.location.href;
var fileName = url.substring(url.lastIndexOf('/') + 1);
// alert(fileName)

function previewFiles(fileList) {
  const container = document.getElementById('result');
  container.innerHTML = '';

  Array.from(fileList).forEach((file) => {
    const reader = new FileReader();
    reader.onload = function (e) {
      const imgContainer = document.createElement('div');
      imgContainer.classList.add('img-container');
      const img = document.createElement('img');
      img.src = e.target.result;
      imgContainer.appendChild(img);
      container.appendChild(imgContainer);
    };
    reader.readAsDataURL(file);
  });
}

function showAlert(message) {
  const alertBox = document.getElementById("customAlert");
  const alertMessage = document.getElementById("alertMessage");

  alertMessage.textContent = message;
  alertBox.style.display = "block";

  setTimeout(() => {
    alertBox.style.display = "none";
  }, 7000);
}


document.addEventListener("DOMContentLoaded", function () {
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById(fileName);


  dropzone.addEventListener("dragover", function (e) {
    e.preventDefault();
    dropzone.classList.add("dragover");
  });

  dropzone.addEventListener("dragleave", function (e) {
    e.preventDefault();
    dropzone.classList.remove("dragover");
  });

  dropzone.addEventListener("change", function (e) {
    e.preventDefault();
    
    const config = fileConfig[fileName];
    if (!config) {
      showAlert(translations.unsupported);
      return;
    }

    const files = Array.from(fileInput.files);
    const validFiles = files.filter(file => config.types.includes(file.type));

    if (validFiles.length === 0) {
      showAlert(config.alertMsg);
      fileInput.value = '';
      return;
    }

    if (validFiles.length > config.maxFiles) {
      // showAlert(`You can upload a maximum of ${config.maxFiles} file(s).`);
      showAlert(`${translations.maxFiles} ${config.maxFiles} ${translations.fileSuffix}`);
      fileInput.value = '';
      return;
    }

    const dataTransfer = new DataTransfer();
    validFiles.forEach(file => dataTransfer.items.add(file));
    fileInput.files = dataTransfer.files;
    
    previewFiles(event.target.files); 
    
  });


  dropzone.addEventListener("drop", function (e) {
    e.preventDefault();
    dropzone.classList.remove("dragover");

    const config = fileConfig[fileName];
    if (!config) {
      showAlert(translations.unsupported);
      return;
    }
    
    const files = e.dataTransfer.files;
    const validFiles = Array.from(files).filter(file => config.types.includes(file.type));

    if (validFiles.length === 0) {
      showAlert(config.alertMsg);
      return;
    }

    if (validFiles.length > config.maxFiles) {
      showAlert(`${translations.maxFiles} ${config.maxFiles} ${translations.fileSuffix}`);
      return;
    }

    const dataTransfer = new DataTransfer();
    validFiles.forEach(file => dataTransfer.items.add(file));
    fileInput.files = dataTransfer.files;

    previewFiles(e.dataTransfer.files);

  });

  dropzone.addEventListener("click", function () {
    fileInput.click();
  });
});


$(document).ready(function () {
  var form_name = '#form' + fileName;
  var btn_download_form = '#btn_download_' + fileName
  
  $('input[name="file"]').on('change', function () {
    $(btn_download_form).css('display', 'none');
  });

  $(form_name).submit(function (event) {
    $('#img_loading').css('display', 'block');
    event.preventDefault()

    var formData = new FormData($(this)[0])
    var csrftoken = getCookie('csrftoken')

    $.ajax({
      type: 'POST',
      url: '/en/'+fileName,
      data: formData,
      processData: false,
      contentType: false,
      headers: {
        'X-CSRFToken': csrftoken
      },
      success: function (response) {
        var download_form = 'download_' + fileName
        if (response.success) {
          
          $(btn_download_form).attr('href','/'+download_form);
          $(btn_download_form).css('display','inline-block');
          $('#img_loading').css('display', 'none');

        } else {
          console.error(response.errors)
          $('#img_loading').css('display', 'none');
        }
      },
      error: function (xhr, status, error) {
        $('#img_loading').css('display', 'none');
        console.error(xhr.responseText)
      }
    })
  })

})

function getCookie(name) {
  var cookieValue = null
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';')
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i])
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-input');
  const formGroup = document.getElementById('search-form-group');

  searchInput.addEventListener('focus', function() {
    formGroup.classList.add('focused');
  });

  searchInput.addEventListener('blur', function() {
    formGroup.classList.remove('focused');
  });
});  

