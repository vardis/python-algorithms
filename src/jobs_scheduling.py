"""
This algorithm takes as input a set of N jobs, each with a given expected duration, and with some
precedence constraints among these jobs. The goal of the algorithm is to schedule these jobs to
run on multiple processors in the order that will guarantee the shortest execution time.

To solve this problem we model the set of jobs with a DAG, the jobs can be scheduled only if there
are no cyclic dependencies among them so a DAG makes sense. Each edge of the graph has a weight equal
to the expected running time of the job that acts as the source node.

The solution to this problem is based on the identification of the critical execution path. This is the
longest path along a sequence of depended jobs that determines that smallest possible completion time.
If we schedule the jobs in the same fashion as they appear in the critical path, we can guarantee that
all the other available processors will be busy to finish as many jobs as possible during that minimum
completion time.

We introduce two artificial vertices s and t, the sink and target vertices. The start vertex s is
connected with the start vertex v of every job using a zero weighted edge. Similarly the target
vertex t is connected with the end vertex w of every job using a zero weighted edge.

"""

from graph_utils import *
import graph_cycle
import dag_shortest_path

def build_graph_from_input():
    f = open('../data/jobs_spec.txt')
    num_jobs = int(f.readline())
    g = WeightedDigraph(num_jobs + 2)

    source_node = num_jobs
    sink_node = num_jobs + 1

    cost_per_job = {}

    for l in f.readlines():
        job_spec = l.split()
        job_id = int(job_spec[0])
        cost = float(job_spec[1])
        depending = job_spec[2:]
        cost_per_job[job_id] = cost

        for dep in depending:
            g.add_weighted_edge(job_id, int(dep), cost)

    cycle_detector = graph_cycle.DirectedCycleDetector(g)
    if cycle_detector.has_cycle():
        print "There's a cyclic dependency between the input jobs"
        print cycle_detector.cycle()
        exit(1)


    for i in range(num_jobs):
        g.add_weighted_edge(source_node, i, 0.0)
        g.add_weighted_edge(i, sink_node, cost_per_job[i])

    # print g
    return g

jobs_dag = build_graph_from_input()

source_vertex = jobs_dag.V() - 2
sink_vertex = source_vertex + 1
dag_sp = dag_shortest_path.DAGShortestPath(jobs_dag)
dag_sp.longest_path(source_vertex)

for i in range(jobs_dag.V() - 2):
    print "Scheduled time for job %d: %f" % (i, dag_sp.distance_to(i))

print "Total running time", dag_sp.distance_to(sink_vertex)


