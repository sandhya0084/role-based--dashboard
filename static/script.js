// Generic modal functions
function openModal(id) {
  document.getElementById(id).style.display = "block";
}
function closeModal(id) {
  document.getElementById(id).style.display = "none";
}
window.onclick = function (e) {
  document.querySelectorAll(".modal").forEach((m) => {
    if (e.target == m) {
      m.style.display = "none";
    }
  });
};
function openEditUserModal(id, username, email, role) {
  document.getElementById("editUserId").value = id;
  document.getElementById("editUsername").value = username;
  document.getElementById("editEmail").value = email;
  document.getElementById("editRole").value = role;
  openModal("editUserModal");
}
function openDeleteUserModal(id) {
  document.getElementById("deleteUserId").value = id;
  openModal("deleteUserModal");
}
function openEditTaskModal(id, title, desc, assigned_to, status) {
  document.getElementById("editTaskId").value = id;
  document.getElementById("editTaskTitle").value = title;
  document.getElementById("editTaskDescription").value = desc;
  document.getElementById("editTaskAssignedTo").value = assigned_to;
  document.getElementById("editTaskStatus").value = status;
  openModal("editTaskModal");
}
function openDeleteTaskModal(id) {
  document.getElementById("deleteTaskId").value = id;
  openModal("deleteTaskModal");
}
