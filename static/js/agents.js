function openForm(event) {
    agent_id = event.target.parentNode.parentNode.childNodes[1].innerText
    document.getElementById('cmd_form').style.display = 'block'
    document.getElementById('form_agent_id').value = agent_id
  }
  
  function closeForm() {
    document.getElementById('cmd_form').style.display = 'none'
  }
  
  function deleteAgent(event) {
    agent_id = event.target.parentNode.parentNode.childNodes[1].innerText
    document.getElementById('delete_agent_field').value = agent_id
    document.delete_agent_form.submit()
  }