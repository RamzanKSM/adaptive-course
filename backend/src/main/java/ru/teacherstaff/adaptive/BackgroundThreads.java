package ru.teacherstaff.adaptive;

import java.util.concurrent.ThreadFactory;

/**
 * Threads for the application's own background work. They are platform (daemon) threads, never virtual ones.
 * <p>
 * The backend runs with one CPU (compose: cpus 1.0), so the JVM gives all virtual threads a single carrier thread.
 * A virtual thread that blocks without unmounting — the Codex App Server reader waiting in a blocking read of the
 * process output did exactly that — holds that only carrier, and every other virtual thread waits: console runs of
 * submissions waited for minutes and went through only when a chat message made Codex print something. Platform
 * threads are scheduled by the OS and cannot starve each other this way.
 */
final class BackgroundThreads {
  private BackgroundThreads() {}

  /** Daemon platform threads named exactly «name». */
  static ThreadFactory named(String name) { return Thread.ofPlatform().daemon().name(name).factory(); }

  /** Daemon platform threads named «prefix0», «prefix1», … */
  static ThreadFactory named(String prefix, long start) { return Thread.ofPlatform().daemon().name(prefix, start).factory(); }
}
