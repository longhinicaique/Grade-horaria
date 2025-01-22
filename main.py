
import pandas as pd
import random
import math
import matplotlib.pyplot as plt
from fpdf import FPDF


# Configurações gerais
dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
horarios_manha = [
    "7:15 - 8:05",
    "8:06 - 8:55",
    "8:56 - 9:45",
    "10:06 - 10:55",
    "10:56 - 11:45",
    "11:46 - 12:30",
]
horarios_tarde = [
    "13:15 - 14:05",
    "14:06 - 14:55", 
    "14:56 - 15:45", 
    "16:06 - 16:55",
    "16:56 - 17:45", 
    "17:46 - 18:30",
]
series_manha = {
    "A": "6º Ano",
    "B": "7º Ano",
    "C": "8º Ano",
    "D": "9º Ano",
    "E": "1º Médio",
    "F": "2º Médio",
    "G": "3º Médio",
}
series_tarde = {
    "H": "6º Ano Tarde",
    "I": "7º Ano Tarde",
    "J": "8º Ano Tarde",
    "K": "9º Ano Tarde",
    "L": "1º Médio Tarde",
    "M": "2º Médio Tarde",
    "N": "3º Médio Tarde",
}

substituicoes_professores = {
    "Alan": "Prof. Alan",
    "Bia": "Prof. Bia",
    "Jady": "Prof. Jady",
    "Miro": "Prof. Miro",
    "Jussara": "Prof. Jussara",
    "Marilza": "Prof. Marilza",
    "Veloso": "Prof. Veloso",
    "Ingrid": "Prof. Ingrid",
    "Nicole": "Prof. Nicole",
    "Marcelo": "Prof. Marcelo",
}

professores_manha = {
    "Alan": {
        "Inglês": list(series_manha.keys()),
        "Português": ["A", "B"]
    },
    "Bia": {
        "Geografia": ["B", "C", "E", "F", "G"],
        "Espanhol": list(series_manha.keys())
    },
    "Jady": {
        "Matemática": list(series_manha.keys()),
        "Finanças": ["E", "F", "G"]
    },
    "Miro": {
        "História": list(series_manha.keys()),
        "Geografia": ["A", "D"]
    },
    "Jussara": {
        "Educação Física": list(series_manha.keys())
    },
    "Marilza": {
        "Literatura": ["C", "D", "E", "F", "G"]
    },
    "Veloso": {
        "Física": ["E", "F", "G"],
        "Maker": list(series_manha.keys())
    },
    "Ingrid": {
        "Biologia": ["E", "F", "G"],
        "Projeto Científico": list(series_manha.keys()),
        "Ambiente": ["E", "F", "G"]
    },
    "Nicole": {
        "Química": ["E", "F", "G"],
    }
}

professores_tarde = {
    "Alan": {
        "Inglês": ["H", "I", "J", "K"],
        "Português": ["H", "I"]
    },
    "Bia": {
        "Geografia": ["I", "J", "L", "M", "N"],
        "Espanhol": ["H", "I", "J", "K"]
    },
    "Jady": {
        "Matemática": ["H", "I", "J", "K"],
        "Finanças": ["L", "M", "N"]
    },
    "Miro": {
        "História": ["H", "I", "J", "K"],
        "Geografia": ["H", "K"]
    },
    "Jussara": {
        "Educação Física": ["H", "I", "J", "K"]
    },
    "Marilza": {
        "Literatura": ["J", "K", "L", "M", "N"]
    },
    "Veloso": {
        "Física": ["L", "M", "N"],
        "Maker": ["H", "I", "J", "K"]
    },
    "Ingrid": {
        "Biologia": ["L", "M", "N"],
        "Projeto Científico": ["H", "I", "J", "K"],
        "Ambiente": ["L", "M", "N"]
    },
    "Nicole": {
        "Química": ["L", "M", "N"],
    },
    "Marcelo": {
        "Musica": ["H", "I", "J", "K"],
    }
}

carga_horaria = {
    "Literatura": 5,
    "Português": 5,
    "Matemática": 5,
    "História": 3,
    "Geografia": 3,
    "Educação Física": 2,
    "Química": 2,
    "Física": 2,
    "Inglês": 3,
    "Espanhol": 3,
    "Finanças": 2,
    "Maker": 2,
    "Biologia": 2,
    "Projeto Científico": 2,
    "Ambiente": 2,
    "Musica": 1,
    "Outros": 2,
}

# Dias em que os professores não estão disponíveis
indisponibilidade_professores_manha = {
    "Alan": [],  # UM EXEMPLO DE COMO USA "Segunda"
    "Bia": [],
    "Jady": [],
    "Miro": [],
    "Jussara": [],
    "Marilza": [],
    "Veloso": [],
    "Ingrid": [],
    "Nicole": [],
    "Marcelo": [],
}

indisponibilidade_professores_tarde = {
    "Alan": [],
    "Bia": [],
    "Jady": [],
    "Miro": [],
    "Jussara": [],
    "Marilza": [],
    "Veloso": [],
    "Ingrid": [],
    "Nicole": [],
    "Marcelo": [],
}

LIMITE_HORAS_SEMANAIS = 40

def inicializar_banco_horarios(horarios, series):
    """Inicializa o banco de horários."""
    return {
        dia: {
            horario: {
                sala: None
                for sala in series.keys()
            }
            for horario in horarios
        }
        for dia in dias_semana
    }

def inicializar_grade(horarios):
    """Inicializa a grade horária para um professor."""
    return pd.DataFrame(index=horarios, columns=dias_semana)

def validar_dados(professores, series):
    """Valida os dados iniciais para evitar inconsistências."""
    erros = []
    for professor, materias in professores.items():
        for materia, turmas in materias.items():
            if materia not in carga_horaria:
                erros.append(
                    f"Matéria {materia} do professor {professor} não tem carga horária definida."
                )
            for turma in turmas:
                if turma not in series:
                    erros.append(
                        f"Turma {turma} do professor {professor} não é válida."
                    )
    if erros:
        raise ValueError("\n".join(erros))

def calcular_custo(grades, professores, horarios):
    """Calcula o custo da solução atual."""
    custo = 0
    carga_horaria_professores = {prof: 0 for prof in professores}
    carga_horaria_materias = {materia: 0 for materia in carga_horaria}

    for professor, grade in grades.items():
        for dia in dias_semana:
            for horario in horarios:
                if not pd.isna(grade.loc[horario, dia]):
                    custo += 1
                    carga_horaria_professores[professor] += 1
                    materia = grade.loc[horario, dia].split('(')[0].strip()
                    carga_horaria_materias[materia] += 1

    # Penalizar se a carga horária passar do limite ou for menor que o necessário
            for professor, carga in carga_horaria_professores.items():
                if carga > LIMITE_HORAS_SEMANAIS:
                    custo += (carga - LIMITE_HORAS_SEMANAIS) * 10  # Penalização alta para excessos
                elif carga < LIMITE_HORAS_SEMANAIS:
                    custo += (LIMITE_HORAS_SEMANAIS - carga) * 10  # Penalização alta para faltas

            for materia, carga in carga_horaria_materias.items():
                if carga > carga_horaria[materia]:
                    custo += (carga - carga_horaria[materia]) * 10  # Penalização alta para excessos
                elif carga < carga_horaria[materia]:
                    custo += (carga_horaria[materia] - carga) * 10  # Penalização alta para faltas

    return custo

def gerar_vizinho(grades, banco_horarios, indisponibilidade_professores, series, professores, horarios):
    """Gera uma solução vizinha ao modificar aleatoriamente uma alocação."""
    novo_grades = {prof: grades[prof].copy() for prof in grades}
    banco_horarios_copy = {
        dia: {
            horario: banco_horarios[dia][horario].copy()
            for horario in banco_horarios[dia]
        }
        for dia in banco_horarios
    }

    professor = random.choice(list(professores.keys()))
    dia = random.choice(dias_semana)
    horario = random.choice(horarios)
    materia = random.choice(list(professores[professor].keys()))
    sala = random.choice(professores[professor][materia])

    if banco_horarios_copy[dia][horario][sala] is None and dia not in indisponibilidade_professores[professor]:
        if pd.isna(novo_grades[professor].loc[horario, dia]):
            novo_grades[professor].loc[horario, dia] = f"{materia} ({series[sala]})\n"
            banco_horarios_copy[dia][horario][sala] = professor
        else:
            turma = novo_grades[professor].loc[horario, dia].split('(')[1].strip(')\n')
            turma_key = [k for k, v in series.items() if v == turma][0]
            banco_horarios_copy[dia][horario][turma_key] = None
            novo_grades[professor].loc[horario, dia] = f"{materia} ({series[sala]})\n"
            banco_horarios_copy[dia][horario][sala] = professor

    return novo_grades, banco_horarios_copy

def simulated_annealing(professores, banco_horarios, grades, indisponibilidade_professores, series, horarios):
    """Resolve o problema de alocação usando Simulated Annealing."""
    temperatura = 100.0
    resfriamento = 0.99
    min_temperatura = 1.0

    current_grades = grades.copy()
    current_custo = calcular_custo(current_grades, professores, horarios)

    while temperatura > min_temperatura:
        novo_grades, novo_banco_horarios = gerar_vizinho(
            current_grades, banco_horarios, indisponibilidade_professores,
            series, professores, horarios)
        novo_custo = calcular_custo(novo_grades, professores, horarios)

        if novo_custo < current_custo:
            current_grades = novo_grades
            banco_horarios = novo_banco_horarios
            current_custo = novo_custo
        else:
            probabilidade = math.exp((current_custo - novo_custo) / temperatura)
            if random.random() < probabilidade:
                current_grades = novo_grades
                banco_horarios = novo_banco_horarios
                current_custo = novo_custo

        temperatura *= resfriamento

    return current_grades

def gerar_grade_completa(professores, series, indisponibilidade_professores, horarios):
    """Gera a grade horária para todos os professores usando Simulated Annealing."""
    validar_dados(professores, series)
    grades = {professor: inicializar_grade(horarios) for professor in professores}

    banco_horarios = inicializar_banco_horarios(horarios, series)

    grades = simulated_annealing(professores, banco_horarios, grades, indisponibilidade_professores, series, horarios)
    return grades

# Gerar a grade e salvar como arquivos CSV
grades_geradas_manha = gerar_grade_completa(professores_manha, series_manha, indisponibilidade_professores_manha, horarios_manha)
grades_geradas_tarde = gerar_grade_completa(professores_tarde, series_tarde, indisponibilidade_professores_tarde, horarios_tarde)

# Verificar se as grades foram geradas corretamente
if grades_geradas_manha:
    print("Grades da manhã geradas com sucesso!")
    for professor, df in grades_geradas_manha.items():
        print(f"Grade da manhã para {professor}:")
        print(df)
else:
    print("Falha ao gerar grades da manhã.")

if grades_geradas_tarde:
    print("Grades da tarde geradas com sucesso!")
    for professor, df in grades_geradas_tarde.items():
        print(f"Grade da tarde para {professor}:")
        print(df)
else:
    print("Falha ao gerar grades da tarde.")

def validar_conflitos(grades_manha, grades_tarde):
    """Valida se há conflitos de horários nas grades horárias da manhã e da tarde."""
    conflitos = []

    # Verificar conflitos na manhã
    for professor, grade in grades_manha.items():
        for dia in dias_semana:
            for horario in horarios_manha:
                if not pd.isna(grade.loc[horario, dia]):
                    sala = grade.loc[horario, dia].split('(')[1].strip(')\n')
                    for outro_professor, outra_grade in grades_manha.items():
                        if professor != outro_professor and not pd.isna(outra_grade.loc[horario, dia]):
                            outra_sala = outra_grade.loc[horario, dia].split('(')[1].strip(')\n')
                            if sala == outra_sala:
                                conflitos.append(f"Conflito na manhã: {dia} {horario} - {professor} e {outro_professor} na sala {sala}")

    # Verificar conflitos na tarde
    for professor, grade in grades_tarde.items():
        for dia in dias_semana:
            for horario in horarios_tarde:
                if not pd.isna(grade.loc[horario, dia]):
                    sala = grade.loc[horario, dia].split('(')[1].strip(')\n')
                    for outro_professor, outra_grade in grades_tarde.items():
                        if professor != outro_professor and not pd.isna(outra_grade.loc[horario, dia]):
                            outra_sala = outra_grade.loc[horario, dia].split('(')[1].strip(')\n')
                            if sala == outra_sala:
                                conflitos.append(f"Conflito na tarde: {dia} {horario} - {professor} e {outro_professor} na sala {sala}")

    return conflitos

# Chamada da função para validar conflitos
conflitos = validar_conflitos(grades_geradas_manha, grades_geradas_tarde)
if conflitos:
    print("Conflitos encontrados:")
    for conflito in conflitos:
        print(conflito)
else:
    print("Nenhum conflito encontrado.")

def exportar_para_csv(grades, nome_arquivo_prefixo):
    """Exporta as grades horárias para arquivos CSV."""
    for professor, df in grades.items():
        professor_nome = substituicoes_professores[professor]
        df.to_csv(f"{nome_arquivo_prefixo}_grade_horaria_{professor_nome}.csv")
    print(f"Grades horárias exportadas para arquivos CSV com prefixo {nome_arquivo_prefixo}")

# Exportar grades para CSV
exportar_para_csv(grades_geradas_manha, "manha")
exportar_para_csv(grades_geradas_tarde, "tarde")


# Substituição de nomes dos professores, se necessário
substituicoes_professores = {
    # "professor_original": "nome_substituido"
}




def exportar_para_ods(grades, nome_arquivo):
    """Exporta as grades horárias para um arquivo ODS."""
    try:
        # Cria um writer para arquivos .ods
        with pd.ExcelWriter(nome_arquivo, engine='odf') as writer:
            for professor, df in grades.items():
                professor_nome = substituicoes_professores.get(professor, professor)
                print(f"Exportando grade para aba: {professor_nome}")
                df.to_excel(writer, sheet_name=professor_nome, index=True)
        print(f"Grades horárias exportadas para {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao exportar para ODS: {e}")

# Exportar as grades para ODS
exportar_para_ods(grades_geradas_manha, "grades_manha.ods")
exportar_para_ods(grades_geradas_tarde, "grades_tarde.ods")


def exportar_para_pdf(grades, nome_arquivo_prefixo):
    """Exporta as grades horárias para um arquivo PDF."""
    pdf = FPDF()

    for professor, df in grades.items():
        # Usando o método get() para evitar o KeyError
        professor_nome = substituicoes_professores.get(professor, professor)

        # Adicionar uma nova página para cada professor
        pdf.add_page()
        pdf.set_font("Arial", size=10)  # Fonte menor para o título

        # Título
        pdf.cell(200, 10, txt=f"Grade Horária: {professor_nome}", ln=True, align='C')

        pdf.set_font("Arial", size=8)  # Fonte menor para o conteúdo
        pdf.ln(10)

        # Definir largura das colunas com base no número de dias da semana
        col_width = pdf.w / (len(dias_semana) + 1)
        row_height = pdf.font_size * 1.5

        # Cabeçalho da tabela
        pdf.cell(col_width, row_height, "Horário", border=1)
        for dia in dias_semana:
            pdf.cell(col_width, row_height, dia, border=1)
        pdf.ln(row_height)

        # Adicionar as linhas da tabela
        for horario in df.index:
            pdf.cell(col_width, row_height, horario, border=1)
            for dia in dias_semana:
                aula = df.loc[horario, dia]
                if pd.isna(aula):
                    aula = ""
                pdf.cell(col_width, row_height, aula, border=1)
            pdf.ln(row_height)

    pdf.output(f"{nome_arquivo_prefixo}_grade_horaria.pdf")
    print(f"Grades horárias exportadas para {nome_arquivo_prefixo}_grade_horaria.pdf")

# Exportar grades para PDF
exportar_para_pdf(grades_geradas_manha, "manha")
exportar_para_pdf(grades_geradas_tarde, "tarde")


# Função para visualizar a carga horária de cada professor
def visualizar_carga_horaria(grades_combinadas_ajustadas):
    carga_horaria_professores = {}
    for professor, grade in grades_combinadas_ajustadas.items():
        total_aulas = grade.notna().sum().sum()
        carga_horaria_professores[professor] = total_aulas

    # Gráfico de barras da carga horária dos professores
    plt.figure(figsize=(18, 6))
    plt.bar(carga_horaria_professores.keys(), carga_horaria_professores.values(), color='skyblue')
    plt.xlabel('Professores')
    plt.ylabel('Carga Horária Total')
    plt.title('Carga Horária Total dos Professores')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Visualizar carga horária para manhã e tarde
visualizar_carga_horaria(grades_geradas_manha)
visualizar_carga_horaria(grades_geradas_tarde)

# Verificação final das cargas horárias
def verificar_carga_horaria(grades, carga_horaria):
    """Verifica se a carga horária de cada matéria está correta."""
    carga_horaria_professores = {prof: 0 for prof in grades}
    carga_horaria_materias = {materia: 0 for materia in carga_horaria}

    for professor, grade in grades.items():
        for dia in dias_semana:
            for horario in grade.index:
                if not pd.isna(grade.loc[horario, dia]):
                    materia = grade.loc[horario, dia].split('(')[0].strip()
                    carga_horaria_materias[materia] += 1
                    carga_horaria_professores[professor] += 1

    for professor, carga in carga_horaria_professores.items():
        if carga != LIMITE_HORAS_SEMANAIS:
            print(f"Aviso: Carga horária do professor {professor} está incorreta! ({carga} horas)")
    
    for materia, carga in carga_horaria_materias.items():
        if carga != carga_horaria[materia]:
            print(f"Erro: {materia} tem {carga} aulas, mas deveria ter {carga_horaria[materia]} aulas.")

# Verificar carga horária para manhã e tarde
verificar_carga_horaria(grades_geradas_manha, carga_horaria)
verificar_carga_horaria(grades_geradas_tarde, carga_horaria)



