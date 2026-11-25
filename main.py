"""
Módulo de Exemplo de Automação
Autor: Luís Philipe (@phlimaz)
Descrição: Script de automação que analisa arquivos em diretórios e gera relatórios automáticos.
"""

from pathlib import Path
from datetime import datetime


def gerar_relatorio_diretorio(caminho_pasta: str = ".") -> dict:
    """Analisa uma pasta e retorna estatísticas dos arquivos encontrados."""
    pasta = Path(caminho_pasta).resolve()
    
    if not pasta.exists() or not pasta.is_dir():
        print(f"❌ Diretório inválido: {pasta}")
        return {}

    total_arquivos = 0
    tamanho_total_bytes = 0
    extensoes = {}

    for item in pasta.rglob("*"):
        if item.is_file():
            total_arquivos += 1
            tamanho_total_bytes += item.stat().st_size
            ext = item.suffix.lower() or "sem_extensao"
            extensoes[ext] = extensoes.get(ext, 0) + 1

    tamanho_mb = tamanho_total_bytes / (1024 * 1024)

    return {
        "pasta": str(pasta),
        "total_arquivos": total_arquivos,
        "tamanho_mb": round(tamanho_mb, 2),
        "extensoes": extensoes,
        "data_execucao": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }


def salvar_relatorio_txt(dados: dict, nome_arquivo: str = "relatorio_execucao.txt") -> Path:
    """Exporta o resumo da análise para um arquivo de texto organizado."""
    caminho = Path(dados["pasta"]) / nome_arquivo
    
    conteudo = [
        "=" * 60,
        " 📄 RELATÓRIO CONSOLIDADO DE ARQUIVOS",
        f" Gerado em: {dados['data_execucao']}",
        "=" * 60,
        f"• Diretório analisado : {dados['pasta']}",
        f"• Total de arquivos   : {dados['total_arquivos']}",
        f"• Espaço ocupado      : {dados['tamanho_mb']} MB",
        "",
        "📊 Distribuição por extensão:",
    ]
    
    for ext, qtd in sorted(dados["extensoes"].items(), key=lambda x: x[1], reverse=True):
        conteudo.append(f"   - {ext:<12}: {qtd} arquivo(s)")
        
    conteudo.extend(["=" * 60, "Fim do relatório."])
    
    caminho.write_text("\n".join(conteudo), encoding="utf-8")
    return caminho


def main():
    print("=" * 60)
    print(" 🚀 Automação de Análise de Arquivos - Início")
    print("=" * 60)

    resultado = gerar_relatorio_diretorio(".")

    if resultado:
        print(f"📁 Pasta analisada : {resultado['pasta']}")
        print(f"📄 Total de arquivos: {resultado['total_arquivos']}")
        print(f"💾 Tamanho total   : {resultado['tamanho_mb']} MB")
        print(f"🕒 Executado em    : {resultado['data_execucao']}")
        print("\n📊 Tipos de arquivos encontrados:")
        for ext, qtd in sorted(resultado['extensoes'].items(), key=lambda x: x[1], reverse=True):
            print(f"   • {ext:<12} : {qtd} arquivo(s)")
            
        arquivo_salvo = salvar_relatorio_txt(resultado)
        print(f"\n💾 Relatório salvo em: {arquivo_salvo.name}")
            
    print("=" * 60)
    print(" ✅ Automação concluída com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    main()
