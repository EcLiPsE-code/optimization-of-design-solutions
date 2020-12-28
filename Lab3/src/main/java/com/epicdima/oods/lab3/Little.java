package com.epicdima.oods.lab3;

import java.util.*;
import java.util.function.Predicate;
import java.util.stream.Collectors;

import static com.epicdima.oods.lab3.Utils.*;

/**
 * @author EpicDima
 */
public class Little {
    public static Utils.Result calculate(int[][] original) {
        final int size = original.length;
        Queue<Branch> branches = new PriorityQueue<>();
        int[][] c = copyArray(original, size);
        List<Node> nodes = new ArrayList<>(size);
        int gamma = cast(c, size, nodes);
        while (nodes.size() < size - 2) {
            int t1 = findMaxZeroPower(c, size, nodes);
            int t2 = cast(c, size, nodes);

            List<Node> nodesRight = new ArrayList<>(nodes);
            nodesRight.remove(nodesRight.size() - 2);
            branches.offer(new Branch(c, size, nodesRight, gamma + t2));

            List<Node> nodesLeft = new ArrayList<>(nodes);
            nodesLeft.remove(nodesLeft.size() - 1);
            int[][] c2 = copyArray(c, size);
            c2[nodesLeft.get(nodesLeft.size() - 1).col][nodesLeft.get(nodesLeft.size() - 1).row] = INF;
            branches.offer(new Branch(c2, size, nodesLeft, gamma + t1));

            Branch best = branches.poll();
            assert best != null;
            c = copyArray(best.c, size);
            nodes = new ArrayList<>(best.nodes);
            gamma = best.gamma;
        }
        addLastNodes(size, nodes);
        List<Integer> resultNodes = fillNodeList(size, nodes);
        return new Utils.Result(resultNodes, calculateDistance(resultNodes, original));
    }

    private static List<Integer> fillNodeList(int size, List<Node> nodes) {
        List<Integer> resultNodes = new ArrayList<>(size);
        int current = nodes.get(0).row;
        resultNodes.add(current);
        for (int i = 0; i < size; i++) {
            for (Node node : nodes) {
                if (node.col == current) {
                    current = node.row;
                    resultNodes.add(current);
                    break;
                }
            }
        }
        return resultNodes;
    }

    private static void addLastNodes(int size, List<Node> nodes) {
        List<Integer> rows = new ArrayList<>(nodes.size());
        List<Integer> cols = new ArrayList<>(nodes.size());
        for (Node node : nodes) {
            rows.add(node.row);
            cols.add(node.col);
        }
        List<Integer> lastRows = new ArrayList<>(2);
        List<Integer> lastCols = new ArrayList<>(2);
        for (int i = 0; i < size; i++) {
            if (!rows.contains(i)) {
                lastRows.add(i);
            }
            if (!cols.contains(i)) {
                lastCols.add(i);
            }
        }
        for (int i = 0, j1 = 0, j2 = 0; i < 2; i++, j1++, j2++) {
            int row = lastRows.get(j1);
            int col = lastCols.get(j2);
            if (row == col) {
                row = lastRows.get(j1 + 1);
                j1--;
            }
            nodes.add(new Node(row, col, true));
        }
    }

    private static int cast(int[][] c, final int size, List<Node> nodes) {
        List<Integer> rows = new ArrayList<>(nodes.size());
        List<Integer> cols = new ArrayList<>(nodes.size());
        for (Node node : nodes) {
            rows.add(node.row);
            cols.add(node.col);
        }
        Predicate<Integer> skipByRows = (it) -> {
            int idx = rows.indexOf(it);
            return idx != -1 && nodes.get(idx).withRemoval;
        };
        Predicate<Integer> skipByCols = (it) -> {
            int idx = cols.indexOf(it);
            return idx != -1 && nodes.get(idx).withRemoval;
        };
        int[] u = new int[size];
        findMinInRows(c, size, u, skipByRows, skipByCols);
        int[] v = new int[size];
        findMinInCols(c, size, v, skipByRows, skipByCols);
        int gamma = 0;
        for (int i = 0; i < size; i++) {
            gamma += u[i];
            gamma += v[i];
        }
        return gamma;
    }

    private static void findMinInCols(int[][] c, int size, int[] v, Predicate<Integer> skipByRows, Predicate<Integer> skipByCols) {
        for (int i = 0; i < size; i++) {
            if (skipByCols.test(i)) {
                continue;
            }
            int min = INF;
            for (int j = 0; j < size; j++) {
                if (!skipByRows.test(j) && c[j][i] < min) {
                    min = c[j][i];
                }
            }
            v[i] = min;
            for (int j = 0; j < size; j++) {
                if (!skipByRows.test(j) && c[j][i] != INF) {
                    c[j][i] -= min;
                }
            }
        }
    }

    private static void findMinInRows(int[][] c, int size, int[] u, Predicate<Integer> skipByRows,
                                      Predicate<Integer> skipByCols) {
        for (int i = 0; i < size; i++) {
            if (skipByRows.test(i)) {
                continue;
            }
            int min = INF;
            for (int j = 0; j < size; j++) {
                if (!skipByCols.test(j) && c[i][j] < min) {
                    min = c[i][j];
                }
            }
            u[i] = min;
            for (int j = 0; j < size; j++) {
                if (!skipByCols.test(j) && c[i][j] != INF) {
                    c[i][j] -= min;
                }
            }
        }
    }

    private static int findMaxZeroPower(int[][] c, final int size, List<Node> nodes) {
        List<Integer> rows = new ArrayList<>(nodes.size());
        List<Integer> cols = new ArrayList<>(nodes.size());
        for (Node node : nodes) {
            rows.add(node.row);
            cols.add(node.col);
        }
        Predicate<Integer> skipByRows = (it) -> {
            int idx = rows.indexOf(it);
            return idx != -1 && nodes.get(idx).withRemoval;
        };
        Predicate<Integer> skipByCols = (it) -> {
            int idx = cols.indexOf(it);
            return idx != -1 && nodes.get(idx).withRemoval;
        };
        int[][] powers = new int[size][size];
        int rowIndex = -1, colIndex = -1;
        int maxPower = Integer.MIN_VALUE;
        for (int i = 0; i < size; i++) {
            if (skipByRows.test(i)) {
                continue;
            }
            Arrays.fill(powers[i], -1);
            for (int j = 0; j < size; j++) {
                if (!skipByCols.test(j) && c[i][j] == 0) {
                    int minPowerInRow = findMinPowerInRow(c, size, skipByCols, i, j);
                    int minPowerInCol = findMinPowerInCol(c, size, skipByRows, i, j);
                    powers[i][j] = 0;
                    if (minPowerInRow != INF) {
                        powers[i][j] += minPowerInRow;
                    }
                    if (minPowerInCol != INF) {
                        powers[i][j] += minPowerInCol;
                    }
                    if (powers[i][j] > maxPower) {
                        maxPower = powers[i][j];
                        rowIndex = i;
                        colIndex = j;
                    }
                }
            }
        }
        c[rowIndex][colIndex] = INF;
        nodes.add(new Node(rowIndex, colIndex, true));
        nodes.add(new Node(rowIndex, colIndex, false));
        return maxPower;
    }

    private static int findMinPowerInCol(int[][] c, int size, Predicate<Integer> skipByRows, int i, int j) {
        int min = INF;
        for (int k = 0; k < size; k++) {
            if (!skipByRows.test(k) && k != i && c[k][j] < min) {
                min = c[k][j];
            }
        }
        return min;
    }

    private static int findMinPowerInRow(int[][] c, int size, Predicate<Integer> skipByCols, int i, int j) {
        int min = INF;
        for (int k = 0; k < size; k++) {
            if (!skipByCols.test(k) && k != j && c[i][k] < min) {
                min = c[i][k];
            }
        }
        return min;
    }


    private static class Node {
        public final int row;
        public final int col;
        public final boolean withRemoval;

        public Node(int row, int col, boolean withRemoval) {
            this.row = row;
            this.col = col;
            this.withRemoval = withRemoval;
        }

        @Override
        public String toString() {
            return "{" +
                    "" + row +
                    ", " + col +
                    ", " + withRemoval +
                    '}';
        }
    }


    private static class Branch implements Comparable<Branch> {
        public final int[][] c;
        public final List<Node> nodes;
        public final int gamma;

        public Branch(int[][] c, int size, List<Node> nodes, int gamma) {
            this.c = copyArray(c, size);
            this.nodes = new ArrayList<>(nodes);
            this.gamma = gamma;
        }

        @Override
        public int compareTo(Branch o) {
            return Integer.compare(gamma, o.gamma);
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Branch branch = (Branch) o;
            return gamma == branch.gamma &&
                    Arrays.equals(c, branch.c) &&
                    nodes.equals(branch.nodes);
        }

        @Override
        public int hashCode() {
            int result = Objects.hash(nodes, gamma);
            result = 31 * result + Arrays.hashCode(c);
            return result;
        }

        @Override
        public String toString() {
            return "{" +
                    "gamma=" + gamma +
                    ", nodes=" + nodes +
                    '}';
        }

        @Override
        protected Object clone() throws CloneNotSupportedException {
            return calculate((int[][]) super.clone());
        }
    }

    /**
     * @author EpicDima
     */
    public static class Inner {
        public static Result calculate(int[][] original) {
            Inner inner = new Inner(original, original.length);
            inner.calculate();
            List<Integer> list = Arrays.stream(inner.route).boxed().collect(Collectors.toList());
            list.add(list.get(0));
            return new Result(list, calculateDistance(list, original));
        }

        private final int[][] original;
        private final int size;
        private final int[] points;
        private int[] route;
        private int minLength = INF;

        private Inner(int[][] original, int size) {
            this.original = original;
            this.size = size;
            this.points = new int[size];
            for (int i = 0; i < size; i++) {
                points[i] = i;
            }
        }

        private void calculate(int i) {
            if (i == size) {
                int length = calculateRouteLength();
                if (length < minLength) {
                    route = Arrays.copyOf(points, size);
                    minLength = length;
                }
            }
            for (int j = i; j < size; j++) {
                swap(points, i, j);
                calculate(i + 1);
                swap(points, i, j);
            }
        }

        private void calculate() {
            calculate(1);
        }

        private int calculateRouteLength() {
            int length = 0;
            for (int i = 1; i <= points.length; i++) {
                length += original[points[i - 1]][points[i % size]];
            }
            return length;
        }

        private static void swap(int[] array, int firstIdx, int secondIdx) {
            int temp = array[firstIdx];
            array[firstIdx] = array[secondIdx];
            array[secondIdx] = temp;
        }
    }
}
