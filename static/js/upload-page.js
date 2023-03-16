const uploadForm = document.getElementById("upload-form")
const dragAndDropInput = document.getElementById("file")
const dragAndDropElement = document.getElementById("drag-and-drop")
const uploadProgress = document.getElementById("upload-progress")
const uploadDuration = document.getElementById("upload_duration")
const maximumAllowedSize = document.getElementById("maximum_allowed_size")

const preventDefaults = (element) => {
  element.preventDefault()
  element.stopPropagation()
}

const handleDrop = (element) => {
  const { files } = element.dataTransfer

  if (files.length !== 1) {
    return
  }

  handleFiles(files)
}

const handleFiles = (files) => {
  dragAndDropInput.files = files

  htmx.on('#upload-form', 'htmx:xhr:progress',
    (event) => htmx
      .find('#upload-progress')
      .setAttribute('value', event.detail.loaded / event.detail.total * 100)
  )

  htmx.on(
    '#upload-form', 'htmx:xhr:loadend', () => uploadProgress.classList.add("invisible")
  )

  uploadForm.requestSubmit()
  uploadProgress.classList.remove("invisible")
}

const handleUploadDurationChange = () => {
  const uploadDurationIndex = parseInt(
    uploadDuration.value, 10
  )
  const {
    maximum_file_size_in_mb: maximumAllowedSizeValue
  } = window.uploadDurations[uploadDurationIndex]

  maximumAllowedSize.innerHTML = maximumAllowedSizeValue.toString()
}

['dragenter', 'dragover', 'dragleave', 'drop', 'click'].forEach(
  (event) => dragAndDropElement.addEventListener(event, preventDefaults, false)
)

dragAndDropElement.addEventListener('drop', handleDrop, false)

uploadDuration.addEventListener("change", handleUploadDurationChange)
const loadInterval = setInterval(() => {
  if (window.uploadDurations) {
    handleUploadDurationChange()
    clearInterval(loadInterval)
  }
}, 100)

