import React, { useState, useEffect } from "react";
import {
  AppShell,
  Title,
  Text,
  Container,
  Group,
  Stack,
  Button,
  Textarea,
  Select,
  NumberInput,
  Paper,
  Badge,
  Loader,
  Alert,
  Grid,
  Card,
  Table,
  Divider,
  ActionIcon,
  Tooltip,
} from "@mantine/core";
import { notifications } from "@mantine/notifications";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faPlus,
  faTrash,
  faSearch,
  faRobot,
  faExclamationTriangle,
  faCheckCircle,
  faInfoCircle,
} from "@fortawesome/free-solid-svg-icons";
import { apiService } from "./services/api";
import type { TextInput, AnalysisState, ModelsResponse } from "./types/api";

function App() {
  const [texts, setTexts] = useState<TextInput[]>([
    { id: "1", content: "", label: "Text 1" },
    { id: "2", content: "", label: "Text 2" },
  ]);
  const [selectedModel, setSelectedModel] = useState<string>("miniLM");
  const [threshold, setThreshold] = useState<number>(0.7);
  const [analysis, setAnalysis] = useState<AnalysisState>({
    isLoading: false,
    result: null,
    error: null,
  });
  const [availableModels, setAvailableModels] = useState<ModelsResponse | null>(
    null
  );

  // Load available models on component mount
  useEffect(() => {
    const loadModels = async () => {
      try {
        const models = await apiService.getAvailableModels();
        setAvailableModels(models);
        setSelectedModel(models.default_model);
      } catch (error) {
        console.error("Failed to load models:", error);
        notifications.show({
          title: "Error",
          message: "Failed to load available models",
          color: "red",
        });
      }
    };

    loadModels();
  }, []);

  const addTextInput = () => {
    const newId = (texts.length + 1).toString();
    setTexts([...texts, { id: newId, content: "", label: `Text ${newId}` }]);
  };

  const removeTextInput = (id: string) => {
    if (texts.length > 2) {
      setTexts(texts.filter((text) => text.id !== id));
    }
  };

  const updateTextContent = (id: string, content: string) => {
    setTexts(
      texts.map((text) => (text.id === id ? { ...text, content } : text))
    );
  };

  const analyzePlagiarism = async () => {
    const nonEmptyTexts = texts.filter((text) => text.content.trim() !== "");

    if (nonEmptyTexts.length < 2) {
      notifications.show({
        title: "Error",
        message: "Please enter at least 2 texts to analyze",
        color: "red",
      });
      return;
    }

    setAnalysis({ isLoading: true, result: null, error: null });

    try {
      const request = {
        texts: nonEmptyTexts.map((text) => text.content),
        model_key: selectedModel,
        threshold: threshold,
      };

      const result = await apiService.analyzePlagiarism(request);

      setAnalysis({
        isLoading: false,
        result: result,
        error: null,
      });

      notifications.show({
        title: "Analysis Complete",
        message: `Found ${result.plagiarized_pairs.length} potential plagiarism cases`,
        color: "green",
      });
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "An unexpected error occurred";
      setAnalysis({
        isLoading: false,
        result: null,
        error: errorMessage,
      });

      notifications.show({
        title: "Analysis Failed",
        message: errorMessage,
        color: "red",
      });
    }
  };

  const getSimilarityColor = (similarity: number) => {
    if (similarity >= 0.8) return "red";
    if (similarity >= 0.6) return "orange";
    if (similarity >= 0.4) return "yellow";
    return "green";
  };

  const renderSimilarityMatrix = () => {
    if (!analysis.result) return null;

    const matrix = analysis.result.similarity_matrix;
    const size = matrix.length;

    return (
      <Card withBorder p="md" mt="md">
        <Title order={3} mb="md">
          <FontAwesomeIcon icon={faInfoCircle} style={{ marginRight: "8px" }} />
          Similarity Matrix
        </Title>
        <Table striped highlightOnHover>
          <Table.Thead>
            <Table.Tr>
              <Table.Th></Table.Th>
              {Array.from({ length: size }, (_, i) => (
                <Table.Th key={i}>Text {i + 1}</Table.Th>
              ))}
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {matrix.map((row, i) => (
              <Table.Tr key={i}>
                <Table.Td>
                  <strong>Text {i + 1}</strong>
                </Table.Td>
                {row.map((similarity, j) => (
                  <Table.Td key={j}>
                    <Badge
                      color={getSimilarityColor(similarity)}
                      variant={i === j ? "filled" : "light"}
                    >
                      {(similarity * 100).toFixed(1)}%
                    </Badge>
                  </Table.Td>
                ))}
              </Table.Tr>
            ))}
          </Table.Tbody>
        </Table>
      </Card>
    );
  };

  const renderPlagiarismResults = () => {
    if (!analysis.result) return null;

    const pairs = analysis.result.plagiarized_pairs;

    return (
      <Card withBorder p="md" mt="md">
        <Title order={3} mb="md">
          <FontAwesomeIcon
            icon={faExclamationTriangle}
            style={{ marginRight: "8px" }}
          />
          Potential Plagiarism Cases ({pairs.length})
        </Title>

        {pairs.length === 0 ? (
          <Alert icon={<FontAwesomeIcon icon={faCheckCircle} />} color="green">
            No plagiarism detected above the threshold of{" "}
            {(threshold * 100).toFixed(1)}%
          </Alert>
        ) : (
          <Stack gap="md">
            {pairs.map((pair, index) => (
              <Paper key={index} p="md" withBorder>
                <Group justify="space-between" mb="sm">
                  <Text fw={500}>
                    Text {pair.index_1 + 1} ↔ Text {pair.index_2 + 1}
                  </Text>
                  <Badge color={getSimilarityColor(pair.similarity)} size="lg">
                    {(pair.similarity * 100).toFixed(1)}% Similar
                  </Badge>
                </Group>
                <Grid>
                  <Grid.Col span={6}>
                    <Text size="sm" c="dimmed" mb="xs">
                      Text {pair.index_1 + 1} Preview:
                    </Text>
                    <Text size="sm" style={{ fontStyle: "italic" }}>
                      "{pair.text_1_preview}..."
                    </Text>
                  </Grid.Col>
                  <Grid.Col span={6}>
                    <Text size="sm" c="dimmed" mb="xs">
                      Text {pair.index_2 + 1} Preview:
                    </Text>
                    <Text size="sm" style={{ fontStyle: "italic" }}>
                      "{pair.text_2_preview}..."
                    </Text>
                  </Grid.Col>
                </Grid>
              </Paper>
            ))}
          </Stack>
        )}
      </Card>
    );
  };

  const renderAnalysisStats = () => {
    if (!analysis.result) return null;

    return (
      <Card withBorder p="md" mt="md">
        <Title order={3} mb="md">
          Analysis Statistics
        </Title>
        <Grid>
          <Grid.Col span={6}>
            <Text size="sm" c="dimmed">
              Model Used:
            </Text>
            <Text fw={500}>{analysis.result.model_used}</Text>
          </Grid.Col>
          <Grid.Col span={6}>
            <Text size="sm" c="dimmed">
              Threshold:
            </Text>
            <Text fw={500}>
              {(analysis.result.threshold_used * 100).toFixed(1)}%
            </Text>
          </Grid.Col>
          <Grid.Col span={6}>
            <Text size="sm" c="dimmed">
              Total Comparisons:
            </Text>
            <Text fw={500}>{analysis.result.total_comparisons}</Text>
          </Grid.Col>
          <Grid.Col span={6}>
            <Text size="sm" c="dimmed">
              Execution Time:
            </Text>
            <Text fw={500}>{analysis.result.execution_time.toFixed(2)}s</Text>
          </Grid.Col>
        </Grid>
      </Card>
    );
  };

  return (
    <AppShell
      navbar={{
        width: 350,
        breakpoint: "sm",
      }}
      header={{ height: 60 }}
      padding="md"
    >
      <AppShell.Header>
        <Group h="100%" px="md" justify="space-between">
          <Group>
            <FontAwesomeIcon icon={faRobot} size="lg" />
            <Title order={2}>Plagiarism Detector</Title>
          </Group>
          <Badge color="blue" variant="light">
            Semantic Similarity Analyzer
          </Badge>
        </Group>
      </AppShell.Header>

      <AppShell.Navbar p="md">
        <Stack gap="md">
          <Title order={3}>Configuration</Title>

          <Select
            label="Embedding Model"
            placeholder="Select model"
            value={selectedModel}
            onChange={(value) => setSelectedModel(value || "miniLM")}
            data={
              availableModels?.available_models.map((model) => ({
                value: model,
                label: availableModels.model_descriptions[model]?.name || model,
              })) || []
            }
          />

          <NumberInput
            label="Similarity Threshold"
            description="Minimum similarity to flag as plagiarism"
            value={threshold}
            onChange={(value) => setThreshold(Number(value) || 0.7)}
            min={0}
            max={1}
            step={0.1}
            decimalScale={2}
          />

          <Divider />

          <Title order={4}>Text Inputs</Title>

          <Stack gap="sm">
            {texts.map((text) => (
              <Group key={text.id} align="flex-start">
                <Textarea
                  placeholder={`Enter ${text.label.toLowerCase()}...`}
                  value={text.content}
                  onChange={(event) =>
                    updateTextContent(text.id, event.currentTarget.value)
                  }
                  minRows={3}
                  style={{ flex: 1 }}
                />
                {texts.length > 2 && (
                  <Tooltip label="Remove text">
                    <ActionIcon
                      color="red"
                      variant="light"
                      onClick={() => removeTextInput(text.id)}
                    >
                      <FontAwesomeIcon icon={faTrash} />
                    </ActionIcon>
                  </Tooltip>
                )}
              </Group>
            ))}
          </Stack>

          <Button
            leftSection={<FontAwesomeIcon icon={faPlus} />}
            variant="light"
            onClick={addTextInput}
            disabled={texts.length >= 10}
          >
            Add Text Input
          </Button>

          <Button
            leftSection={<FontAwesomeIcon icon={faSearch} />}
            onClick={analyzePlagiarism}
            loading={analysis.isLoading}
            disabled={texts.filter((t) => t.content.trim()).length < 2}
            size="md"
          >
            Analyze Plagiarism
          </Button>
        </Stack>
      </AppShell.Navbar>

      <AppShell.Main>
        <Container size="xl">
          <Stack gap="md">
            <Title order={2}>Analysis Results</Title>

            {analysis.isLoading && (
              <Card withBorder p="xl" style={{ textAlign: "center" }}>
                <Loader size="lg" />
                <Text mt="md" c="dimmed">
                  Analyzing texts for semantic similarity...
                </Text>
              </Card>
            )}

            {analysis.error && (
              <Alert
                icon={<FontAwesomeIcon icon={faExclamationTriangle} />}
                color="red"
              >
                {analysis.error}
              </Alert>
            )}

            {analysis.result && (
              <>
                {renderAnalysisStats()}
                {renderSimilarityMatrix()}
                {renderPlagiarismResults()}
              </>
            )}

            {!analysis.result && !analysis.isLoading && !analysis.error && (
              <Card withBorder p="xl" style={{ textAlign: "center" }}>
                <FontAwesomeIcon
                  icon={faInfoCircle}
                  size="3x"
                  style={{ opacity: 0.3 }}
                />
                <Text mt="md" c="dimmed">
                  Enter at least 2 texts in the sidebar and click "Analyze
                  Plagiarism" to get started.
                </Text>
              </Card>
            )}
          </Stack>
        </Container>
      </AppShell.Main>
    </AppShell>
  );
}

export default App;
