(() => {
  const dialog = document.getElementById('new-cupboard-dialog');
  const openButton = document.getElementById('open-cupboard-dialog');
  const closeButton = document.getElementById('close-cupboard-dialog');
  const cancelButton = document.getElementById('cancel-cupboard-dialog');
  const nameInput = document.getElementById('new-cupboard-name');

  if (!dialog || !openButton) return;

  openButton.addEventListener('click', () => {
    dialog.showModal();
    nameInput.focus();
  });

  function closeDialog() {
    dialog.close();
    openButton.focus();
  }

  closeButton.addEventListener('click', closeDialog);
  cancelButton.addEventListener('click', closeDialog);
})();
