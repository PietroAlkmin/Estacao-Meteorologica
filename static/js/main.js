function deletarLeitura(id) {
    if (confirm(`Tem certeza que deseja deletar a leitura #${id}?`)) {
        fetch(`/leituras/${id}/deletar`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'deletado') {
                const row = document.getElementById(`row-${id}`);
                if (row) row.remove();
                alert('Leitura deletada com sucesso!');
            } else {
                alert('Erro ao deletar leitura.');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Ocorreu um erro de rede ao tentar deletar.');
        });
    }
}
