const uploadForm = document.getElementById("upload-form")
const dragAndDropInput = document.getElementById("file")
const dragAndDropElement = document.getElementById("drag-and-drop")
const uploadProgress = document.getElementById("upload-progress")

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

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(
  (event) => dragAndDropElement.addEventListener(event, preventDefaults, false)
)

dragAndDropElement.addEventListener('drop', handleDrop, false)
