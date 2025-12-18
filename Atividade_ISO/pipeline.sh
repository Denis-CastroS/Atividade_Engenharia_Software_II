#!/bin/bash
# ==========================================================
# Pipeline de Montagem de Genoma (SPAdes) e Anotação (Prokka)
# Projeto fictício avaliado segundo a norma ISO/IEC 9126
# Autor: Dupla de desenvolvimento (com apoio de IA)
# ==========================================================

# -----------------------------
# CONFIGURAÇÕES INICIAIS
# -----------------------------
THREADS=4
OUTDIR="resultado_pipeline"
SPADES_OUT="$OUTDIR/spades"
PROKKA_OUT="$OUTDIR/prokka"

# -----------------------------
# FUNÇÃO DE USO
# -----------------------------
uso() {
    echo "Uso: $0 <reads_R1.fastq> <reads_R2.fastq> <nome_organismo>"
    echo "Exemplo: $0 sample_R1.fastq sample_R2.fastq Escherichia_coli"
    exit 1
}

# -----------------------------
# VERIFICAÇÃO DE PARÂMETROS
# -----------------------------
if [ $# -ne 3 ]; then
    echo "[ERRO] Número incorreto de parâmetros."
    uso
fi

READ1=$1
READ2=$2
ORGANISMO=$3

# -----------------------------
# VERIFICAÇÃO DE DEPENDÊNCIAS
# -----------------------------
echo "[INFO] Verificando dependências..."

for prog in spades.py prokka; do
    if ! command -v $prog &> /dev/null; then
        echo "[ERRO] Programa '$prog' não encontrado no sistema."
        exit 1
    fi
done

# -----------------------------
# VERIFICAÇÃO DE ARQUIVOS
# -----------------------------
if [ ! -f "$READ1" ] || [ ! -f "$READ2" ]; then
    echo "[ERRO] Arquivos de leitura não encontrados."
    exit 1
fi

# -----------------------------
# CRIAÇÃO DE DIRETÓRIOS
# -----------------------------
mkdir -p "$SPADES_OUT" "$PROKKA_OUT"

# -----------------------------
# ETAPA 1 – MONTAGEM COM SPADES
# -----------------------------
echo "[INFO] Iniciando montagem do genoma com SPAdes..."

spades.py \
    -1 "$READ1" \
    -2 "$READ2" \
    -t "$THREADS" \
    -o "$SPADES_OUT"

if [ $? -ne 0 ]; then
    echo "[ERRO] Falha na montagem com SPAdes."
    exit 1
fi

CONTIGS="$SPADES_OUT/contigs.fasta"

if [ ! -f "$CONTIGS" ]; then
    echo "[ERRO] Arquivo contigs.fasta não gerado."
    exit 1
fi

echo "[INFO] Montagem concluída com sucesso."

# -----------------------------
# ETAPA 2 – ANOTAÇÃO COM PROKKA
# -----------------------------
echo "[INFO] Iniciando anotação genômica com Prokka..."

prokka \
    --outdir "$PROKKA_OUT" \
    --prefix "$ORGANISMO" \
    --cpus "$THREADS" \
    "$CONTIGS"

if [ $? -ne 0 ]; then
    echo "[ERRO] Falha na anotação com Prokka."
    exit 1
fi

# -----------------------------
# FINALIZAÇÃO
# -----------------------------
echo "=========================================="
echo "[SUCESSO] Pipeline executado com sucesso!"
echo "Resultados disponíveis em: $OUTDIR"
echo "Montagem: $SPADES_OUT"
echo "Anotação: $PROKKA_OUT"
echo "=========================================="

exit 0
